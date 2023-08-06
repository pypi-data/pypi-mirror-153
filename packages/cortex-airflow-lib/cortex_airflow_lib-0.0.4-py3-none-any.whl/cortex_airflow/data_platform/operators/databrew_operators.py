from airflow.models import BaseOperator
from cortex_airflow.data_platform.utils.aws_utils import DataBrewClient


class DatabrewProfilerOperator(BaseOperator):
    def __init__(self, task_id, job_name, retries=1, **kwargs) -> None:
        """
        :param task_id: id of the this task
        :param job_name name of the profile job to run
        :param kwargs: all kwargs will be forwarded to the BaseOperator as parameters
        """
        self.job_name = job_name
        super().__init__(task_id=task_id, retries=retries, **kwargs)


    def execute(self, context):
        databrew_client = DataBrewClient()
        databrew_client.start_databrew_profiling_job(job_name=self.job_name)
