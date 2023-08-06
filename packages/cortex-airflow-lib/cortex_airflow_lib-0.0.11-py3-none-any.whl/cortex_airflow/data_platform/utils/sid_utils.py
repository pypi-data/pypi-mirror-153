import json
import pandas as pd
from http import HTTPStatus
from numpy import datetime64
import requests

from cortex_airflow.data_platform.utils import time_utils
from cortex_airflow.data_platform.utils import http_utils

import logging

session = http_utils.requests_retry_session()
SID_MIN_DATE = datetime64('1800-01-01 00:00:00')
SID_MAX_DATE = datetime64('2100-01-01 00:00:00')


def get_sid_token(auth_endpoint, sid_user, user_password):
    credentials = {"login": sid_user, "password": user_password}

    response = session.post(auth_endpoint, json=credentials)

    if response.status_code == 200:
        response_json = response.json()
        return response_json["key"]
    if response.status_code != 200:
        logging.info("response ", response)
        time_utils.sleep(60)
        get_sid_token(auth_endpoint, sid_user, user_password)


def get_execution_id(load_manager, token, data_input_id):
    headers = get_auth_header(token=token)

    execution_id = ""

    if execution_id == "":
        execution_id = _get_execution_id(load_manager, headers, data_input_id)

    return execution_id


def get_data_input_id(load_manager, token, cubo_id):
    headers = get_auth_header(token=token)

    data_input_id = ""

    if data_input_id == "":
        data_input_id = _get_data_input_id(load_manager, headers, cubo_id)

    return data_input_id


def start_execution_process(load_manager, token, execution_id, current_try=0, max_tries=5):
    if current_try >= max_tries:
        raise TimeoutError(f'Failed execution process more than the max allowed: {max_tries}')
    logging.info(" try start_execution_process ")
    headers = get_auth_header(token=token)
    endpoint = load_manager + "/execution/" + execution_id + "/start"

    response = session.put(endpoint, headers=headers)

    if response.status_code == 200:
        logging.info(" Start Data Input Process ")
    elif response.status_code == 400:
        logging.info(" Error on start_execution_process ", response.status_code)
        logging.info("response ", response.json())
    else:
        logging.info(" Error on start_execution_process ", response.status_code)
        logging.info("response ", response)
        time_utils.sleep(60)
        start_execution_process(load_manager, token, execution_id, current_try=current_try + 1, max_tries=max_tries)


def check_completed_execution_id(platform_url, username, password, execution_id: str):
    loadmanager = '	https://api.cortex-intelligence.com'
    credentials = {"login": username, "password": password}
    auth_endpoint = f"https://{platform_url}/service/integration-authorization-service.login"

    response = requests.post(auth_endpoint, json=credentials)
    response_json = response.json()
    try:
        headers = {"Authorization": "Bearer " + response_json["key"]}
    except KeyError:
        raise ValueError(f'Wrong response: {response_json}')
    endpoint = loadmanager + "/execution/" + execution_id
    response = requests.get(endpoint, headers=headers)

    if response.status_code != HTTPStatus.OK:
        raise ValueError(f'It was expected a {HTTPStatus.OK} http status code, it was received: {response.status_code} '
                         f'\n {response.text}')
    response_json = response.json()
    return response_json


def __squash_date_column(df, column):
    df[column] = pd.to_datetime(df[column], errors='coerce').dt.normalize()
    df.loc[df[column] > SID_MAX_DATE, column] = SID_MAX_DATE
    df.loc[df[column] < SID_MIN_DATE, column] = SID_MIN_DATE
    return df


def process_date_columns(df, date_columns):
    for date_column in date_columns:
        __squash_date_column(df, column=date_column)
    return df


def reorder_df_to_sid(df):
    '''
    O SID realiza o parse das primeiras 500 linhas da coluna para determinar qual e o tipo (data, texto, numero) e formato da coluna.
    Essa funcao reoordena as linhas de maneira a trazer os valores nao nulos para o topo do DataFrame, facilitando assim, o parsing pelo SID.
    :param df: DataFrame a ser reordenado
    :return: DataFrame reordenado
    '''
    df = df.reset_index()
    target_rows = set()
    for col in df.columns:
        target_row = df.loc[:, col].first_valid_index()
        if target_row is not None and target_row >= 500:
            target_rows.add(target_row)
    idx = list(target_rows) + [i for i in range(len(df)) if i not in target_rows]
    df = df.iloc[idx]

    return df


def check_execution_process(load_manager, token, execution_id: str):
    headers = get_auth_header(token=token)
    endpoint = load_manager + "/execution/" + execution_id

    response = session.get(endpoint, headers=headers)

    if response.status_code == 200:
        response_json = response.json()
        completed = response_json["completed"]
        if completed is False:

            if 'files' in response_json and 'filesProcessed' in response_json:
                files = response_json['files']
                filesProcessed = response_json['filesProcessed']
                logging.info(f'files {files}, files processed {filesProcessed}')
            time_utils.sleep(30)
            check_execution_process(load_manager, token, execution_id)
        else:
            success = response_json["success"]
            if success is False:
                logging.info(response_json)
                raise ValueError('Error performing the check_execution_process, success is False:')
            else:
                logging.info(" Data Input Processed wirh SUCCESS ")

    if response.status_code != 200:
        time_utils.sleep(60)
        check_execution_process(load_manager, token, execution_id)


def load_csv(load_manager, token: str, execution_id: str, csv_content: str):
    """Load csv file on SID

    Parameters
    ----------
    token : str
        token
    csv_content : str
        csv_content
    cubo_id : str
        cubo_id
    """

    headers = get_auth_header(token=token)

    _upload_file(load_manager, headers, csv_content, execution_id)


def get_auth_header(token):
    if not token:
        token = get_sid_token()

    headers = {"Authorization": "Bearer " + token}

    return headers


def _get_data_input_id(load_manager, headers, cubo_id: str, current_try=0, max_tries=5):
    if current_try >= max_tries:
        raise TimeoutError(f'Failed data input request more than the max allowed: {max_tries}')

    content = {

        "destinationId": cubo_id,

        "fileProcessingTimeout": 600000,

        "executionTimeout": 1200000,

        "ignoreValidationErrors": False,
    }

    endpoint = load_manager + "/datainput"

    response = session.post(endpoint, headers=headers, json=content)

    if response.status_code == 200:
        response_json = response.json()
        return response_json["id"]
    if response.status_code != 200:
        time_utils.sleep(60)
        _get_data_input_id(load_manager, headers, cubo_id, current_try=current_try + 1, max_tries=max_tries)


def _get_execution_id(load_manager, headers, data_input_id: str, current_try=0, max_tries=5):
    if current_try >= max_tries:
        raise TimeoutError(f'Failed execution_id request more than the max allowed: {max_tries}')

    endpoint = load_manager + "/datainput/" + data_input_id + "/execution"
    execution_parameters = {
        'name': 'Data Platform - Airflow',
    }

    response = session.post(endpoint, headers=headers, json=execution_parameters)

    if response.status_code == 200:
        response_json = response.json()
        return response_json["executionId"]
    if response.status_code != 200:
        time_utils.sleep(60)
        _get_execution_id(load_manager, headers, data_input_id, current_try=current_try + 1, max_tries=max_tries)


def _upload_file(load_manager, headers, csv_content, execution_id: str):
    endpoint = load_manager + "/execution/" + execution_id + "/file"

    data = {
        "charset": "UTF-8",
        "quote": '"',
        "escape": "",
        "delimiter": ",",
        "fileType": "CSV",
        "encode": "UTF-8",
    }

    response = session.post(
        url=endpoint, headers=headers, data=data, files={"file": csv_content}
    )

    if response.status_code == 200:
        pass
    elif response.status_code == 400:
        logging.info(f'Error performing the request _upload_file: {response.status_code}')
        logging.info(f'response.json(): {response.json()}')
    else:
        logging.info(f'Error performing the request _upload_file: {response.status_code}')
        logging.info(f'response: {response}')
        time_utils.sleep(120)
        _upload_file(load_manager, headers, csv_content, execution_id)


def upload_file(platform_url, cube_id, username, password, file_like_object):
    url = f'https://{platform_url}/service/integration-authorization-service.login'
    loadmanager = 'https://api.cortex-intelligence.com'
    token = get_sid_token(auth_endpoint=url, sid_user=username, user_password=password)
    headers = get_auth_header(token)
    data_format = {
        "charset": "UTF-8",
        "quote": '"',
        "escape": "\\",
        "delimiter": ",",
        "fileType": "CSV"
    }

    data_input_id = _get_data_input_id(load_manager=loadmanager, headers=headers, cubo_id=cube_id)
    execution_id = _get_execution_id(load_manager=loadmanager, headers=headers, data_input_id=data_input_id)
    endpoint = f"{loadmanager}/execution/{execution_id}/file"
    requests.post(
        endpoint,
        headers=headers,
        data=data_format,
        files={"file": file_like_object},
    )
    start_execution_process(load_manager=loadmanager, token=token, execution_id=execution_id)

    return execution_id


def platform_login(platform_url, login, password):
    url = f'https://{platform_url}/service/integration-authorization-service.login'
    credentials = {"login": login, "password": password}
    response = requests.post(url, json=credentials)
    response = response.json()

    user_id = response['userId']
    key = response['key']
    headers = {'x-authorization-user-id': user_id, 'x-authorization-token': key}

    return headers


def delete_from_cube(cube_id, platform_url, username, password, filters: list = None, auth_header=None):
    if auth_header is None:
        auth_header = platform_login(platform_url, username, password)
    if filters is None:
        filters = [{"name": "# Records", "type": "SIMPLE", "value": 1}]

    url = f'https://{platform_url}/service/integration-cube-service.delete'
    cube = {"id": cube_id}
    cube = json.dumps(cube)
    filters = json.dumps(filters)

    params = {'cube': cube, 'filters': filters}
    response = requests.get(url, params=params, headers=auth_header)

    if response.status_code != HTTPStatus.OK:
        raise ValueError(f'It was expect status code 200, it was received: {response.status_code}\n {response.content}')


def rearrange_df_to_sid(df: pd.DataFrame):
    '''
    O SID realiza o parse das primeiras 500 linhas da coluna para determinar qual e o tipo (data, texto, numero) e formato da coluna.
    Essa funcao reoordena as linhas de maneira a trazer os valores nao nulos para o topo do DataFrame, facilitando assim, o parsing pelo SID.
    :param df: DataFrame a ser reordenado
    :return: DataFrame reordenado
    '''
    df = df.reset_index()
    target_rows = set()
    for col in df.columns:
        target_row = df.loc[:, col].first_valid_index()
        if target_row is not None and target_row >= 500:
            target_rows.add(target_row)
    idx = list(target_rows) + [i for i in range(len(df)) if i not in target_rows]
    df = df.iloc[idx]

    return df

def get_sid_csv(df, **pandas_kwargs) -> str:
    csv_buffer = io.StringIO()

    df.to_csv(csv_buffer, index=False, encoding='utf-8', quoting=csv.QUOTE_NONNUMERIC, **pandas_kwargs)
    csv_value = csv_buffer.getvalue()
    csv_value = csv_value.replace('\\""',
                                  '\\"')  # FIXME: Enquanto o SID escapa as aspas fora do padrao, demanda-se, esse replace
    return csv_value

if __name__ == '__main__':
    import pandas as pd
    import io
    import csv

    url = 'salesdata.cortex-intelligence.com'
    cube_id = '859e27988fc94061b1f14f0f2b4811fd'
    username = 'dataplatform'
    password = 'bj6YueoyuP9eD9mWQ5DSZ1CUQw14TOjMLAoWqvDSDQkOMpfmguWWOtlokBP1pFcfqID54UjFoyzqH4eJUToHMnpS42teCH3L20b'
    file_path = 'vrau.csv'

    df = pd.read_parquet('data/')
    string_buffer = io.BytesIO()
    df.to_csv(string_buffer, index=False, encoding='utf-8', quoting=csv.QUOTE_NONNUMERIC)
    string_buffer.seek(0)

    print('UPLOAD STARTED')
    execution_id = upload_file(platform_url=url, cube_id=cube_id, username=username, password=password,
                               file_like_object=string_buffer)
    print(execution_id)

    resp = check_completed_execution_id(platform_url=url, username=username, password=password,
                                        execution_id='60f3ebef-bbb1-4abf-b2ca-bd9a21d9b93f')
    print(resp)



