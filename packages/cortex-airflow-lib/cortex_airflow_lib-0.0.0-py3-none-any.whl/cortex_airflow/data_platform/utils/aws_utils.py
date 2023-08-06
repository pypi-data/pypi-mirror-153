import base64
import logging
import os
import boto3
import json
from botocore.config import Config
from botocore.errorfactory import ClientError


logger = logging.getLogger(__name__)
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
        self.client = boto3.client(
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
        self.client = boto3.client('databrew', region_name='us-east-1')

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
