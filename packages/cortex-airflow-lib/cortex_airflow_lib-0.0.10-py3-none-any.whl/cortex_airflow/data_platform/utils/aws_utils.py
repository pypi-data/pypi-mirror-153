import base64
import os
import awswrangler as wr
import boto3
import json
from botocore.config import Config
from botocore.errorfactory import ClientError
from cortex_airflow.data_platform.utils import time_utils
from dados_abertos_cnpj.src.configs import logger, app_cfg

from airflow.exceptions import AirflowFailException


DEFAULT_REGION = 'us-east-1'

config = Config(
    retries = {
        'max_attempts': 10,
        'mode': 'standard'
    }
)
class SecretsManager:
    def __init__(self, secret_name, region_name=DEFAULT_REGION, **kwargs):
        if region_name == None:
            region_name = 'us-east-1'
        session = boto3.session.Session()
        self.client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )
        self.secret_name = secret_name

    def get_secret(self):
        try:
            get_secret_value_response = self.client.get_secret_value(
                SecretId=self.secret_name
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'DecryptionFailureException':
                raise e
            elif e.response['Error']['Code'] == 'InternalServiceErrorException':
                raise e
            elif e.response['Error']['Code'] == 'InvalidParameterException':
                raise e
            elif e.response['Error']['Code'] == 'InvalidRequestException':
                raise e
            elif e.response['Error']['Code'] == 'ResourceNotFoundException':
                raise e
        else:
            if 'SecretString' in get_secret_value_response:
                secrets = json.loads(get_secret_value_response['SecretString'])
                return secrets

            else:
                decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
                return decoded_binary_secret

class S3:
    def __init__(self, bucket_name, region_name=DEFAULT_REGION):
        self.bucket_name = bucket_name
        self.s3_client = boto3.client(
            's3',
            region_name=region_name
        )

    @staticmethod
    def build_s3_uri(s3_bucket: str, s3_key: str):
        return f's3://{s3_bucket}/{s3_key}'

    def upload_s3_file(self, path, s3_key, meta_tags=None):
        if meta_tags is None:
            meta_tags = dict()
        extra_args = {"Metadata": meta_tags}
        self.s3_client.upload_file(path, self.bucket_name, s3_key, ExtraArgs=extra_args)

    def download_s3_file(self, s3_path, path):
        self.s3_client.download_file(self.bucket_name, s3_path, path)

    def delete_file(self, s3_path):
        self.s3_client.delete_object(Bucket=self.bucket_name, Key=s3_path)

    def delete_files(self, prefix):
        paginator = self.s3_client.get_paginator('list_objects_v2')
        for result in paginator.paginate(Bucket=self.bucket_name, Delimiter='/', Prefix=prefix):
            if result.get('Contents') is not None:
                for file in result.get('Contents'):
                    self.delete_file(s3_path=file['Key'])

    def list_s3_files(self, prefix='', delimiter=''):
        files = self.s3_client.list_objects_v2(Prefix=prefix, Bucket=self.bucket_name, Delimiter=delimiter)
        return files

    def upload_file_obj(self, file_obj, s3_key, s3_additional_kwargs=None):
        if s3_additional_kwargs is None:
            s3_additional_kwargs = dict()
        self.s3_client.upload_fileobj(Fileobj=file_obj, Bucket=self.bucket_name, Key=s3_key, **s3_additional_kwargs)

    def put_object(self, data, s3_key, s3_additional_kwargs=None):
        if s3_additional_kwargs is None:
            s3_additional_kwargs = dict()
        self.s3_client.put_object(Body=data, Bucket=self.bucket_name, Key=s3_key, **s3_additional_kwargs)

    def get_object(self, s3_path):
        obj = self.s3_client.get_object(Bucket=self.bucket_name, Key=s3_path)
        return obj['Body']

    def download_dir(self, prefix, local=None):
        if local is None:
            local = os.getcwd()
        paginator = self.s3_client.get_paginator('list_objects_v2')
        for result in paginator.paginate(Bucket=self.bucket_name, Delimiter='/', Prefix=prefix):
            if result.get('CommonPrefixes') is not None:
                for subdir in result.get('CommonPrefixes'):
                    self.download_dir(subdir.get('Prefix'), local)
            if result.get('Contents') is not None:
                directory = result.get('Contents')[0]['Key']
                if not os.path.exists(os.path.dirname(local + os.sep + directory)):
                    os.makedirs(os.path.dirname(local + os.sep + directory))
                for file in result.get('Contents'):
                    self.s3_client.download_file(self.bucket_name, file.get('Key'), local + os.sep + file.get('Key'))

    def generate_presigned_url(self, bucket, key, method='put_object', expires_in=300):
        self.s3_client.generate_presigned_url(method, Params={'Bucket': bucket, 'Key': key}, ExpiresIn=expires_in)


class DataBrewClient:
    def __init__(self):
        self.client = session.client('databrew', region_name='us-east-1')

    def start_databrew_profiling_job(self, job_name):
        response = self.client.start_job_run(
            Name=job_name
        )

        return response


class DynamoDB:
    def __init__(self, table_name, region_name=DEFAULT_REGION):
        self.dynamo_db = boto3.resource('dynamodb', region_name=region_name)
        self.table = self.dynamo_db.Table(table_name)

    def put_item(self, item):
        response = self.table.put_item(Item=item)
        return response

    def get_item(self, key):
        response = self.table.get_item(Key=key)
        return response['Item']

    def update_item(self, key, update_values):
        update_expression = {k: f":{k.split('.')[-1]}" for k, v in update_values.items()}
        expression_values = {v: update_values[k] for k, v in update_expression.items()}
        update_expression = 'set ' + ','.join([f'{k}={v}' for k, v in update_expression.items()])
        response = self.table.update_item(Key=key,
                                          UpdateExpression=update_expression,
                                          ExpressionAttributeValues=expression_values,
                                          ReturnValues="UPDATED_NEW"
                                          )
        return response

    def query(self, expression):
        response = self.table.query(IndexName='s3_bucket-s3_key-index',
                                    KeyConditionExpression=expression
                                    )
        return response['Items']

    def get_all(self):
        res = self.table.scan()
        data = res['Items']

        while res.get('LastEvaluatedKey'):
            response = self.table.scan(ExclusiveStartKey=res['LastEvaluatedKey'])
            data.extend(response['Items'])

        return data


session = boto3.Session(
    aws_access_key_id=app_cfg.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=app_cfg.AWS_SECRET_ACCESS_KEY,
    region_name=DEFAULT_REGION
)

def s3_send_file_by_filepath(filepath, s3path: str) -> None:
    """Send file to S3

    Parameters
    ----------
    filepath : str
        path of the file to be sent 
    s3path : str
        destination path on S3
    """
    s3 = session.client('s3', config=config)
    with open(filepath, "rb") as f:
        s3.upload_fileobj(f, app_cfg.RAW_LAYER, s3path)

def s3_send_file_by_file_obj(file, layer, s3path: str) -> None:
    """Send file to S3

    Parameters
    ----------
    file_obj : File
        File to be sent 
    s3path : str
        destination path on S3
    """
    s3 = session.client('s3', config=config)
    s3.upload_fileobj(file, layer, s3path)


def s3_send_file_by_filepath(filepath, s3path, layer_path: str) -> None:
    """Send file to S3

    Parameters
    ----------
    filepath : str
        path of the file to be sent 
    s3path : str
        destination path on S3
    """
    s3 = session.client('s3', config=config)
    with open(filepath, "rb") as f:
        s3.upload_fileobj(f, layer_path, s3path)


def s3_check_if_file_exists(bucket, key: str) -> bool:
    """check if file exists S3

    Parameters
    ----------
    filepath : str
        path of the file to be sent 
    s3path : str
        destination path on S3
    """
    s3 = session.client('s3', config=config)
    try:
        head = s3.head_object(Bucket=bucket, Key=key)
        print('File exists on S3')
        return True
    except ClientError:
        return False


def s3_check_if_path_exists(bucket, path: str) -> bool:
    """check if path exists S3

    Parameters
    ----------
    filepath : str
        bucket of the path to be check 
    path : str
        destination path on S3
    """

    client = session.client('s3')
    result = client.list_objects(Bucket=bucket, Prefix=path )

    exist = False
    if "Contents" in result:
        exist = True
    else:
        exist = False

    return exist    


def glue_run_job(job_name: str) -> None:
    """Run glue job

    Parameters
    ----------
    job_name : str
        name of the job to execute 
    """
    glue = session.client(service_name='glue', region_name='us-east-1',
        endpoint_url='https://glue.us-east-1.amazonaws.com')

    newJobRun = glue.start_job_run(JobName=job_name)

    job_running = True

    while job_running == True:
        status = glue.get_job_run(JobName=job_name, RunId=newJobRun['JobRunId'])
        job_run_status = status['JobRun']['JobRunState']
        if job_run_status in ["STARTING", "RUNNING", "STOPPING", "STOPPED"] :
            logger.info("job_run_status %s, %s", job_name, job_run_status)
            time_utils.sleep(60)
            continue
        elif job_run_status == "SUCCEEDED":
            logger.info("job_run_status %s", job_run_status)
            job_running == False 
            break
        else:
            logger.info("job_run_status %s", job_run_status)
            raise AirflowFailException("Error on execute glue job " + job_name)


def glue_get_crawler_metrics(crawler_name: str) -> None:
    """Get crawler metrics

    Parameters
    ----------
    crawler_name : str
        name of the glue crawler
    """

    glue = session.client(service_name='glue', region_name='us-east-1',
        endpoint_url='https://glue.us-east-1.amazonaws.com')
 
    response = glue.start_crawler(
        Name=crawler_name
    )
    logger.info("response %s", response)
          
    crawler_running = True

    while crawler_running == True:
        
        response = glue.get_crawler(
            Name=crawler_name
        )
        crawler_status = response['Crawler']['State']
        if crawler_status == "RUNNING" or crawler_status == "STOPPING":
            logger.info("crawler_status %s, %s", crawler_name, crawler_status)
            time_utils.sleep(60)
            continue
        elif crawler_status == "READY":
            logger.info("crawler_status %s", crawler_status)
            crawler_running == False 
            break
        else:
            logger.info("crawler_status %s", crawler_status)
            raise AirflowFailException("Error on execute glue crawler " + crawler_name)
    

def s3_get_list_objects(bucket, s3_prefix: str) -> None:
    """Get list of objects on S3

    Parameters
    ----------
    bucket : str
        bucket name
    s3_prefix : str
        destination path on S3
    """

    s3 = session.client('s3', config=config)
    response = s3.list_objects(
        Bucket=bucket,
        MaxKeys=1000,
        Prefix=s3_prefix,
    )
    
    contents = response['Contents']
    return contents


def wr_s3_read_parquet_as_pandas_df(s3file_path: str):
    """Read parquet file on S3

    Parameters
    ----------     
    s3file_path : str
        destination path on S3
    """
    df = wr.s3.read_parquet(path=s3file_path, boto3_session=session)    

    return df


def wr_s3_read_json_as_pandas_df(s3file_path: str):
    """Read parquet file on S3

    Parameters
    ----------     
    s3file_path : str
        destination path on S3
    """
    df = wr.s3.read_json(path=s3file_path, boto3_session=session)    

    return df


def wr_s3_read_parquet(s3file_path: str, chunked: int):
    """Read parquet file on S3

    Parameters
    ----------     
    s3file_path : str
        destination path on S3
    chunked : int
        chunk size for read
    """
    dfs = wr.s3.read_parquet(path=[s3file_path], chunked=chunked, boto3_session=session)    

    return dfs
    

def wr_s3_read_csv(s3file_path, sep, column_names: str):
    """Read csv file on S3

    Parameters  
    ----------     
    s3file_path : str
        destination path on S3
    chunked : int
        sep char for read
    """
    df = wr.s3.read_csv(path=s3file_path, sep=sep, header=None, names=column_names, boto3_session=session)    

    return df
    

def wr_s3_to_parquet(df, path):
    """write parquet file on S3

    Parameters
    ----------     
    s3file_path : str
        destination path on S3
    chunked : int
        sep char for read
    """
    wr.s3.to_parquet(df=df,path=path, boto3_session=session)    


def wr_s3_to_parquet_governed(df, path, process):    
    wr.s3.to_parquet(
        df=df,
        dataset=True,
        path=path,
        compression=None,
        mode='overwrite',
        database='curated_correios_dev',  # Athena/Glue database
        table=process,  # Athena/Glue table
        table_type='ICEBERG',
        boto3_session=session,
)


def wr_athena_start_query(sql):
    query_exec_id = wr.athena.start_query_execution(sql=sql, boto3_session=session, workgroup='AmazonAthenaIcebergPreview')
    return query_exec_id


def wr_athena_get_query_execution(query_exec_id):
    res = wr.athena.get_query_execution(query_execution_id=query_exec_id, boto3_session=session)
    return res

def glue_run_crawler(crawler_name: str):
    """Run glue job

    Parameters
    ----------
    crawler_name : str
        name of the glue crawler
    """

    glue = session.client(service_name='glue', region_name='us-east-1',
        endpoint_url='https://glue.us-east-1.amazonaws.com')
 
    response = glue.start_crawler(
        Name=crawler_name
    )

    if response['ResponseMetadata']['HTTPStatusCode'] == 200:   
        return response
    else:
        return {}
          

def glue_get_crawler(crawler_name: str):
    """Get crawler metrics

    Parameters
    ----------
    crawler_name : str
        name of the glue crawler
    """

    glue = session.client(service_name='glue', region_name='us-east-1',
        endpoint_url='https://glue.us-east-1.amazonaws.com')
 
    response = glue.get_crawler(
        Name=crawler_name
    )
    
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:   
        return response
    else:
        return {}
    
 
def get_secret(secret_name):
    client = session.client(
        service_name='secretsmanager',
        region_name=DEFAULT_REGION
    )

    get_secret_value_response = client.get_secret_value(
        SecretId=secret_name
    )   

    if 'SecretString' in get_secret_value_response:
        secrets = json.loads(get_secret_value_response['SecretString'])
        return secrets

    raise AirflowFailException('Error on get secret manager ', secret_name)


def s3_download_file(bucket, key, filename: str) -> None:
    """Download file from S3

    Parameters
    ----------
    bucket : str
        The name of the bucket to download from
    key : str
        The name of the key to download from
    filename : str
        The path to the file to download to
    """

    s3 = session.client('s3', config=config)
    s3.download_file(bucket, key, filename)


def wr_s3_to_parquet_catalog_table(df, path, database, table):    
    wr.s3.to_parquet(
        df=df,
        dataset=True,
        path=path,
        compression=None,
        mode='overwrite',
        database=database,  # Athena/Glue database
        table=table,  # Athena/Glue table
        boto3_session=session,
)