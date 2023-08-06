from airflow.hooks.base import BaseHook
from airflow.providers.slack.hooks.slack_webhook import SlackWebhookHook
from airflow.models import Variable

"""
How to use this script:
1.  Create an Slack App and enable Incoming Webhooks.
2.  Allow your app to post messages to the workspace by adding the webhook to it.
3.  Import the function bellow in your DAG python script:
    from utils.slack_utils import notify_slack_task_failed
4.  Set on the default_args dict the following argument, so the function will notify Slack:
    default_args = {
        'on_failure_callback': notify_slack_task_failed
    }
"""

# Connection params (HTTP):
SLACK_CONN_ID = 'slack_alerts'
AIRFLOW_USER = 'airflow'

SLACK_NOTIFY_CONFIG = Variable.get('SLACK_NOTIFY_CONFIG', deserialize_json=True)
SLACK_NOTIFY_ENV = Variable.get('ENVIRONMENT')
SLACK_CHANNEL = SLACK_NOTIFY_CONFIG['slack_channel']
SLACK_WEBHOOK_TOKEN = BaseHook.get_connection(SLACK_CONN_ID).password


# Import this function in your DAG script:
def notify_slack_task_failed(context):
    """Sends a message to a Slack channel that an Airflow DAG task has failed."""
    if SLACK_NOTIFY_ENV == 'PROD':
        slack_msg = f"""
                :red_circle: Task Failed.
                *Task*: {context.get('task_instance').task_id}
                *Dag*: {context.get('task_instance').dag_id}
                *Execution Time*: {context.get('execution_date')}
                *Log Url*: {context.get('task_instance').log_url}
                """

        slack_webhook = SlackWebhookHook(
            http_conn_id=SLACK_CONN_ID,
            username=AIRFLOW_USER,
            webhook_token=SLACK_WEBHOOK_TOKEN,
            channel=SLACK_CHANNEL,
            message=slack_msg
        )
        slack_webhook.execute()
