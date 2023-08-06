from datetime import date, timedelta
from time import perf_counter
import awswrangler as wr
import pandas as pd
import boto3
import re
import os

# TRACKING FUNCTIONS


def tracking(funcao):
    def wrapper(*args, **kwargs):
        _start_step = perf_counter()
        print(f'|-- {funcao.__name__}')

        df = funcao(*args, **kwargs)

        _finish_step = perf_counter()
        if df is not None:
            print(
                f'|---- data shape: rows[{df.shape[0]}] | columns[{df.shape[1]}]')
            print(
                f'|---- data size: {"%.2f" % round(df.memory_usage(deep=True).sum() / 1000000,2)} MB')
        print(
            f'|---- elapsed time: {"%.2f" % round(_finish_step-_start_step,2)} secs')

        return df

    return wrapper


def check_processed_data(monitoring_file, partition):
    if os.path.exists(monitoring_file):
        dates = pd.read_csv(monitoring_file)['date'].to_list()
        date = convert_partition_to_date(partition)
        result = True if date in dates else False
        return result


def monitor(df, monitor, monitoring_file, partition):

    monitor['date'] = convert_partition_to_date(partition)
    monitor = {k: [v] for k, v in monitor.items()}
    monitor = pd.DataFrame.from_dict(monitor)

    duplicate_key = 'date'
    if os.path.exists(monitoring_file):
        monitor = consolidate(monitor, monitoring_file, duplicate_key)
    monitor.to_csv(monitoring_file, index=False)

    return df

# AWS FUNCTIONS


def connect_to_aws(aws_access_key_id,aws_secret_access_key):
    return boto3.session.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name='us-east-1'
    )


@tracking
def drop_aws_temp_table(table_name, my_session, **kwargs):
    wr.athena.start_query_execution(
        """DROP TABLE `{}`;""".format(table_name),
        database="export",
    )


@tracking
def create_aws_temp_table(table_name, awss3path, my_session, **kwargs):
    wr.athena.start_query_execution(
        """CREATE EXTERNAL TABLE IF NOT EXISTS `export`.`{}`
        ( `data` string)
        ROW FORMAT DELIMITED LOCATION '{}'""".format(table_name, awss3path),
        database="export",
    )


@tracking
def get_aws_temp_table_data(table_name, my_session, **kwargs):
    collect = True
    while collect:
        try:
            df = (
                wr.athena.read_sql_table(
                    table=table_name,
                    database="export",
                )
            )
        except:
            print('### RETRY ATHENA ###')
            continue

        collect = False

    return df


@tracking
def get_records_aws_temp_table(table_name, awss3path, my_session, **kwargs):
    return wr.athena.read_sql_query(
        sql=f"select count(*) as records from {table_name}",
        database="export",
    )

# ENVIROMENT FUNCTIONS


def create_bot_folder(datapack, bot):
    os.makedirs(f'{datapack}/{bot}', exist_ok=True)

# PARSING FUNCTIONS


def convert_to_snakecase(data):
    for k, v in data.copy().items():
        _snake_case = re.sub(r'(?<!^)(?=[A-Z])', '_', k).lower()
        data[_snake_case] = data.pop(k)
    return data


def standardize(data, lowers=[], exclude=[]):
    for col in list(data.keys()):
        if col in lowers:
            data[col] = data[col].lower() if type(
                data[col]) == str else data[col]

        elif col in exclude:
            del data[col]

        else:
            data[col] = data[col].upper() if type(
                data[col]) == str else data[col]
    return data


def normalize_multivalues(data):
    for k, v in data.items():
        if type(v) is dict:
            data[k] = '|'.join([f'{k1}-{v1}'for k1, v1 in v.items()])
    return data

def normalize_tag(data,tag):
    if data.get(tag):
        for k,v in data[tag].items():
            data[k] = v
    return data

# CONSOLITATION FUNCTIONS


@tracking
def consolidate(df, file, duplicate_key):
    _dtype = {'cnpj': 'str'}

    if os.path.exists(file):
        final = pd.read_csv(file, dtype=_dtype)
        df = pd.concat([df, final], ignore_index=True)
        df.drop_duplicates(subset=duplicate_key, inplace=True)

    df.to_csv(file, index=False)
    return df

# DATE FUNCTIONS


def get_partitions_between_dates(start_date, end_date, **kwargs):
    partitions = []
    for delta in range((end_date-start_date).days):
        _date = start_date+timedelta(days=delta)
        partition = f'year={_date.strftime("%Y")}/month={_date.strftime("%m")}/day={_date.strftime("%d")}'
        partitions.append(partition)

    return partitions


def get_partitions(method, **kwargs):
    if method == 'yesterday':
        _date = date.today() - timedelta(days=1)
        return [f'year={_date.strftime("%Y")}/month={_date.strftime("%m")}/day={_date.strftime("%d")}']
    if method == 'today':
        _date = date.today()
        return [f'year={_date.strftime("%Y")}/month={_date.strftime("%m")}/day={_date.strftime("%d")}']
    if method == 'range':
        return get_partitions_between_dates(**kwargs)


def convert_partition_to_date(partition):
    partition = partition.replace('year=', '')
    partition = partition.replace('month=', '')
    partition = partition.replace('day=', '')
    partition = partition.replace('/', '-')
    return partition

# PROCESSING DATA

def process_data(datapack,bot,duplicate_key,partitions,awss3path,parse_function,final_file,session_credentials):
    my_session = connect_to_aws(**session_credentials)
    
    for partition in partitions:
        credentials = {
            'table_name': bot,
            'awss3path': f'{awss3path}/{datapack}/{bot}/{partition}',
            'my_session': my_session
        }

        print(f'RUNNING {bot} - {partition}')

        drop_aws_temp_table(**credentials)
        create_aws_temp_table(**credentials)
        df = get_aws_temp_table_data(**credentials)
        df = parse_function(df, duplicate_key)
        df = consolidate(df, final_file, duplicate_key)
        del df