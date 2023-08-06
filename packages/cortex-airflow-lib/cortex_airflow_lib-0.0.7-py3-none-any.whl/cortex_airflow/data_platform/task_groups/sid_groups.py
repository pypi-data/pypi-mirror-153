from airflow.models import Variable, clear_task_instances
from airflow.operators.python import PythonOperator
from airflow.utils.session import provide_session
from airflow.utils.task_group import TaskGroup

from cortex_airflow.data_platform.operators.sid_operators import SidOperator, SID_MAX_ROWS
from cortex_airflow.data_platform.sensors.sid_sensors import SidSensor
from cortex_airflow.data_platform.utils import aws_utils
from cortex_airflow.data_platform.utils import sid_utils
import json
import pandas as pd

from io import StringIO

import logging

def create_sid_groups_flow(pipe_control_var, trusted_layer_path):
    """Create tasks to delivery data by SID

    Parameters
    ----------
    pipe_control_var : str
        Airflow variable responsible for controlling pipeline
    """
    with TaskGroup('sid') as sid_group:

        pipeline_control = Variable.get(pipe_control_var, deserialize_json=True)

        aux_task = {}
        count = 0
        for sink_name in pipeline_control["sid"]["sinks"]:

            with TaskGroup(sink_name) as sid_task:
                is_processed = get_sink_status(pipe_control_var, sink_name)
                if is_processed == True:
                    continue
                task_get_execution_id = PythonOperator(
                    task_id='get_execution_id',
                    provide_context=True,
                    do_xcom_push=True,
                    python_callable=prepare_sid_env_task,
                    op_kwargs={'pipe_control_var': pipe_control_var,
                               'trusted_layer_path': trusted_layer_path,
                               'sink_name': sink_name}
                )

                trusted_layer_files = get_layer_files_to_process(pipe_control_var, trusted_layer_path, sink_name)
                task_upload_files = create_task_send_files(trusted_layer_files)
                task_sensor_file = create_task_sensor_file(pipe_control_var)

                task_get_execution_id >> task_upload_files >> task_sensor_file

            # to organize tasks
            if count > 0:
                aux_task >> sid_task
            aux_task = sid_task
            count += 1

    return sid_group


def create_sid_upload_flow(task_id, platform_url: str, username: str, password: str, cube_id: str, python_callable, op_kwargs=None, ignore_empty_dataframe=False,
                           sleep_between_chunks=30, sid_chunksize=SID_MAX_ROWS, date_columns=None, pandas_kwargs=None):
    with TaskGroup(task_id) as sid_group:
        sid_operator = SidOperator(task_id=f'operator', cube_id=cube_id, platform_url=platform_url, username=username, password=password, python_callable=python_callable,
                                   op_kwargs=op_kwargs, ignore_empty_dataframe=ignore_empty_dataframe, sleep_between_chunks=sleep_between_chunks, sid_chunksize=sid_chunksize,
                                   date_columns=date_columns, pandas_kwargs=pandas_kwargs)
        sid_sensor = SidSensor(task_id=f'sensor', platform_url=platform_url, sid_operator=sid_operator)

        sid_operator >> sid_sensor

    return sid_group


def get_sink_status(pipe_control_var, sink_name):
    pipeline_control = Variable.get(pipe_control_var, deserialize_json=True)
    is_processed = pipeline_control["sid"]["sinks"][sink_name]["processed"]
    return is_processed


def set_sink_status_to_true(pipe_control_var, sink_name):
    pipeline_control = Variable.get(pipe_control_var, deserialize_json=True)
    pipeline_control["sid"]["sinks"][sink_name]["processed"] = True
    Variable.set(pipe_control_var, json.dumps(pipeline_control, indent=4))


def prepare_sid_env_task(pipe_control_var, trusted_layer_path, sink_name, **context):
    """Prepare env to send files to SID    

    Parameters
    ----------
    sink_name : str
        sink name on pipeline control
    """
    pipeline_control = Variable.get(pipe_control_var, deserialize_json=True)
    sid_process_config = pipeline_control["sid"]["sinks"][sink_name]

    auth_endpoint = pipeline_control["sid"]["auth_endpoint"]
    load_manager = pipeline_control["sid"]["load_manager"]
    secret_name = pipeline_control["sid"]["secret_name"]

    secrets = aws_utils.get_secret(secret_name)
    sid_user = secrets["login"]
    user_password = secrets["password"]

    sid_token = sid_utils.get_sid_token(auth_endpoint, sid_user, user_password)

    sid_data_input_id = sid_utils.get_data_input_id(
        load_manager,
        sid_token,
        sid_process_config["cubo_id"])

    sid_execution_id = sid_utils.get_execution_id(
        load_manager,
        sid_token,
        sid_data_input_id)

    context['ti'].xcom_push(key='sid_token', value=sid_token)
    context['ti'].xcom_push(key='sid_execution_id', value=sid_execution_id)
    context['ti'].xcom_push(key='trusted_layer_path', value=trusted_layer_path)

    sid_file_chunk = sid_process_config['sid_file_chunk']
    sid_file_begin = sid_process_config['sid_file_begin']
    sid_file_end = sid_process_config['sid_file_end']

    context['ti'].xcom_push(key='sid_file_chunk', value=sid_file_chunk)
    context['ti'].xcom_push(key='sid_file_begin', value=sid_file_begin)
    context['ti'].xcom_push(key='sid_file_end', value=sid_file_end)
    context['ti'].xcom_push(key='load_manager', value=load_manager)
    context['ti'].xcom_push(key='sink_name', value=sink_name)


def get_layer_files_to_process(pipe_control_var, trusted_layer_path, sink_name):
    """Get S3 files objects   

    Parameters
    ----------
    sink_name : str
        sink name on pipeline control
    """
    pipeline_control = Variable.get(pipe_control_var, deserialize_json=True)
    sid_process_config = pipeline_control["sid"]["sinks"][sink_name]
    base_date = pipeline_control["base_date"]

    year = base_date.split('-')[0]
    month = base_date.split('-')[1]
    prefix = "{}year={}/month={}".format(sid_process_config['s3_prefix'], year, month)

    trusted_layer_files = aws_utils.s3_get_list_objects(
        trusted_layer_path,
        prefix)

    return trusted_layer_files


def create_task_send_files(trusted_layer_files):
    send_files_task = PythonOperator(
                task_id='task_send_files',
                python_callable=_task_send_file,
                op_kwargs={'files': trusted_layer_files},
                provide_context=True,
            )
    return send_files_task


def create_task_sensor_file(pipe_control_var):
    sensor_file_task = PythonOperator(
                task_id='sensor_sid_file',
                python_callable=_task_sensor_file,
                op_kwargs={'pipe_control_var':pipe_control_var},
                provide_context=True,
            )
    return sensor_file_task


def _task_send_file(files, **context):
    s3_path = context['ti'].xcom_pull(key='trusted_layer_path')
    logging.info("create_task_send_files %s", s3_path)

    sid_token = context['ti'].xcom_pull(key='sid_token')
    sid_execution_id = context['ti'].xcom_pull(key='sid_execution_id')
    sid_file_chunk = context['ti'].xcom_pull(key='sid_file_chunk')
    sid_file_begin = context['ti'].xcom_pull(key='sid_file_begin')
    sid_file_end = context['ti'].xcom_pull(key='sid_file_end')
    load_manager = context['ti'].xcom_pull(key='load_manager')
    print(sid_execution_id)

    count = 0
    for file in files:

        count += 1

        if count >= sid_file_end:
            break

        if count >= sid_file_begin:
            print('send file {} of {}'.format(count, len(files)))
            file_path = file['Key']
            s3_file_path = 's3://{}/{}'.format(s3_path, file_path)
            # s3://cortex-data-platform-trusted-area-dev/receita_federal/dados_abertos_cnpj/empresas/run-1632755590381-part-block-0-r-00000-snappy.parquet
            chunked=sid_file_chunk

            dfs = aws_utils.wr_s3_read_parquet(s3_file_path, chunked)

            for df in dfs:
                df = rearrange_df_to_sid(df)
                _upload_df_on_sid(load_manager, df, sid_token, sid_execution_id)



def _task_sensor_file(pipe_control_var, **context):

    sid_token = context['ti'].xcom_pull(key='sid_token')
    sid_execution_id = context['ti'].xcom_pull(key='sid_execution_id')
    load_manager = context['ti'].xcom_pull(key='load_manager')
    sink_name = context['ti'].xcom_pull(key='sink_name')

    logging.info(f'execution_id {sid_execution_id}')

    sid_utils.start_execution_process(load_manager=load_manager,
                                      token=sid_token,
                                      execution_id=sid_execution_id
                                      )

    sid_utils.check_execution_process(load_manager=load_manager,
                                      token=sid_token,
                                      execution_id=sid_execution_id
                                      )
    set_sink_status_to_true(pipe_control_var, sink_name)

def reorganize_df(df):
    """Reorganize df by date column with more missing values  

    Parameters
    ----------
    df : pd.DataFrame
        pandas dataframe
    """
    columns = df.columns
    max_missing = 1000000
    max_missing_col = ""
    for col in columns:

        diff = len(df) - len(df[df[col].str.len() == 0])
        if 'data_' in col:
            if diff < max_missing and diff != 0:
                max_missing = diff
                max_missing_col = col

    if max_missing_col != "":
        df = df.sort_values(by=[max_missing_col], ascending=False)

    return df


def normalize_dates_pattern(df):
    """Check and update date column with wrong values to the SID

    Parameters
    ----------
    df : pd.DataFrame
        pandas dataframe
    """
    columns = df.columns
    for col in columns:

        if 'data_' in col:
            index = df[(df[col] != '') & (df[col] < '18000101')].index
            df.loc[index, col] = '18000101'
            index = df[(df[col] != '') & (df[col] > '21000101')].index
            df.loc[index, col] = '21000101'

    return df


def rearrange_df_to_sid(df: pd.DataFrame):
    '''
    O SID realiza o parse das primeiras 500 linhas da coluna para determinar qual e o tipo (data, texto, numero) e formato da coluna.
    Essa funcao reoordena as linhas de maneira a trazer os valores nao nulos para o topo do DataFrame, facilitando assim, o parsing pelo SID.
    :param df: DataFrame a ser reordenado
    :return: DataFrame reordenado e com datas checadas
    '''
    df = normalize_dates_pattern(df)
    df = reorganize_df(df)

    return df


def _upload_df_on_sid(load_manager, df, sid_token, sid_execution_id):
    """Make a CSV of df and send to SID"""
    csv_buffer = StringIO()

    df.to_csv(csv_buffer,
        header=True,
        index=False,
        quoting=1,
        quotechar="\"",
        escapechar="")

    sid_utils.load_csv(
        load_manager=load_manager,
        token=sid_token,
        execution_id=sid_execution_id,
        csv_content = csv_buffer.getvalue())

