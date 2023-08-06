import io
import collections
import logging
import pandas as pd
import time
import csv
from airflow.operators.python import PythonOperator

from cortex_airflow.data_platform.utils.sid_utils import process_date_columns, reorder_df_to_sid, upload_file

SID_MAX_ROWS = 10000000
log = logging.getLogger(__name__)


class SidOperator(PythonOperator):
    def __init__(self, task_id, cube_id, platform_url: str, username: str, password: str, python_callable, op_kwargs=None, ignore_empty_dataframe=False, sleep_between_chunks=30,
                 sid_chunksize=SID_MAX_ROWS, date_columns=None, pandas_kwargs=None, retries=2, **kwargs) -> None:
        """
        :param task_id: id of the this task
        :param cube_id: id of the cube to be stored the data
        :param platform_url: id of the platform to be stored the data
        :param python_callable: it is expected a Callable that returns a pandas DataFrame or else a TypeError will be raised
        :param op_kwargs: python_callable kwargs
        :param ignore_empty_dataframe: will consider a empty dataframe as a success
        :param kwargs: all kwargs will be forwarded to the PythonOperator as parameters
        """
        if op_kwargs is None:
            op_kwargs = dict()
        if pandas_kwargs is None:
            pandas_kwargs = dict()
        if date_columns is None:
            date_columns = list()

        super().__init__(task_id=task_id, python_callable=python_callable, op_kwargs=op_kwargs, retries=retries, **kwargs)
        self.cube_id = cube_id
        self.platform_url = platform_url
        self.username = username
        self.password = password
        self.ignore_empty_dataframe = ignore_empty_dataframe
        self.pandas_kwargs = pandas_kwargs
        self.sleep_between_chunks = sleep_between_chunks
        self.date_columns = date_columns
        self.sid_chunksize = sid_chunksize

    def process_date_columns(self, df):
        process_date_columns(df, date_columns=self.date_columns)
        return df

    def __upload_df_to_sid(self, df, pandas_kwargs=None):
        if pandas_kwargs is None:
            pandas_kwargs = dict()
        df = reorder_df_to_sid(df)
        df = self.process_date_columns(df)
        string_buffer = io.StringIO()
        df.to_csv(string_buffer, index=False, encoding='utf-8', quoting=csv.QUOTE_NONNUMERIC, **pandas_kwargs)
        string_buffer.seek(0)

        log.info(f'UPLOADING DATAFRAME TO SID - SHAPE: {df.shape}')
        execution_id = upload_file(platform_url=self.platform_url,
                                   cube_id=self.cube_id,
                                   username=self.username,
                                   password=self.password,
                                   file_like_object=string_buffer
                                   )

        return execution_id

    def __upload_pandas_df_to_sid(self, df, pandas_kwargs=None):
        if pandas_kwargs is None:
            pandas_kwargs = dict()
        rows = df.shape[0]
        execution_ids = list()

        if rows <= self.sid_chunksize:
            execution_id = self.__upload_df_to_sid(df=df, pandas_kwargs=pandas_kwargs)
            execution_ids.append(execution_id)
        else:
            list_df = [df[i:i + self.sid_chunksize] for i in range(0, df.shape[0], self.sid_chunksize)]
            for i, df_element in enumerate(list_df):
                execution_id = self.__upload_df_to_sid(df=df_element, pandas_kwargs=pandas_kwargs)
                execution_ids.append(execution_id)
                time.sleep(self.sleep_between_chunks)

        return execution_ids

    def upload_df_to_sid(self, df, pandas_kwargs=None):
        if pandas_kwargs is None:
            pandas_kwargs = dict()
        if isinstance(df, pd.DataFrame):
            return self.__upload_pandas_df_to_sid(df=df, pandas_kwargs=pandas_kwargs)
        else:
            raise TypeError(f'df must be a pandas DataFrame object, it is type: {type(df)}')

    def __execute_df(self, df):
        if not isinstance(df, pd.DataFrame):
            raise TypeError(f'The callable must return a pandas DataFrame object, it returned: {type(df)}')

        if self.ignore_empty_dataframe and df.shape[0] == 0:
            return []
        elif not self.ignore_empty_dataframe and df.shape[0] == 0:
            raise ValueError(f'The dataframe passed is empty {df.shape}, please use a valid dataframe')

        execution_ids = self.upload_df_to_sid(df, pandas_kwargs=self.pandas_kwargs)

        return execution_ids

    def execute(self, context):
        df = super().execute(context)
        execution_ids = list()
        if isinstance(df, collections.Iterator):
            for df_part in df:
                execution_id = self.__execute_df(df=df_part)
                execution_ids.extend(execution_id)
        else:
            execution_id = self.__execute_df(df=df)
            execution_ids.extend(execution_id)
        if not self.ignore_empty_dataframe and not execution_ids:
            raise ValueError('There were no dataframes written to SID. Please check if your dataframes are empty')
        log.info(execution_ids)

        context['task_instance'].xcom_push(key='execution_ids', value=execution_ids)
        context['task_instance'].xcom_push(key='platform_url', value=self.platform_url)
        context['task_instance'].xcom_push(key='credentials', value={'username': self.username, 'password': self.password})
