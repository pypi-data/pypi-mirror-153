from cortex_airflow.data_platform.utils.slack_utils import notify_slack_task_failed

# Import this dict in your DAG script:
# from cortex_airflow.data_platform.utils.airflow_utils import DEFAULT_ARGS
#
# Copy the dict variable to yours:
# default_args = DEFAULT_ARGS.copy()
#
# Don't forget to add the start_date argument:
# default_args['start_date'] = <interval schedule>

DEFAULT_ARGS = {
    'depends_on_past': False,
    'owner': 'data_platform',
    'on_failure_callback': notify_slack_task_failed,
}
