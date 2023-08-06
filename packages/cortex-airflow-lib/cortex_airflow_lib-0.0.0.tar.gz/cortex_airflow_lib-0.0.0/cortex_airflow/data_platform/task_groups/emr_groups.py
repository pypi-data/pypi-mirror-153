from airflow.models import Variable
from airflow.providers.amazon.aws.operators.emr_add_steps import EmrAddStepsOperator
from airflow.providers.amazon.aws.operators.emr_create_job_flow import EmrCreateJobFlowOperator
from airflow.providers.amazon.aws.sensors.emr_step import EmrStepSensor
from airflow.utils.task_group import TaskGroup

REGION_NAME = Variable.get('REGION', default_var='us-east-1')
ENVIRONMENT = Variable.get('ENVIRONMENT')


def __generate_emr_steps(name, action_on_failure='CANCEL_AND_WAIT', args=None):
    if args is None:
        args = list()
    SPARK_STEPS = [
        {
            'Name': name,
            'ActionOnFailure': action_on_failure,
            'HadoopJarStep': {
                'Jar': 'command-runner.jar',
                'Args': args
            }
        }
    ]

    return SPARK_STEPS


def create_emr_cluster_flow(task_id,
                            spark_job_paths,
                            release_label='emr-6.4.0',
                            instance_type='m5.xlarge',
                            master_count=1,
                            worker_count=2,
                            retries=2,
                            jobs_kwargs: [list, dict] = None,
                            job_flow_id: str = None,
                            **kwargs
                            ):
    S3_BUCKET = f'cortex-data-platform-mwaa-{ENVIRONMENT}'
    LOG_URI = f's3://{S3_BUCKET}/spark_logs/{task_id}/'

    JOB_FLOW_OVERRIDES = {
            'Name': f'data-platform-airflow-{ENVIRONMENT}-{task_id}',
            'LogUri': LOG_URI,
            'ReleaseLabel': release_label,
            'Applications': [
                {'Name': 'Spark'},
                {'Name': 'Hadoop'},
                {'Name': 'Hive'}
            ],
            'Configurations': [
                {
                    "Classification": "spark-hive-site",
                    "Properties": {
                        "hive.metastore.client.factory.class": "com.amazonaws.glue.catalog.metastore.AWSGlueDataCatalogHiveClientFactory",
                        "hive.metastore.schema.verification": "false"
                    }
                }
            ],
            'Instances': {
                'InstanceGroups': [
                    {
                        'Name': "Master nodes",
                        'Market': 'ON_DEMAND',
                        'InstanceRole': 'MASTER',
                        'InstanceType': instance_type,
                        'InstanceCount': master_count,
                    },
                    {
                        'Name': "Slave nodes",
                        'Market': 'ON_DEMAND',
                        'InstanceRole': 'CORE',
                        'InstanceType': instance_type,
                        'InstanceCount': worker_count,
                    }
                ],
                'KeepJobFlowAliveWhenNoSteps': False,
                'TerminationProtected': False,
            },
            'VisibleToAllUsers': True,
            'JobFlowRole': 'EMR_EC2_DefaultRole',
            'ServiceRole': 'EMR_DefaultRole',
        **kwargs
        }

    with TaskGroup(task_id) as emr_task_group:
        # criar cluster se necessario
        if not job_flow_id:
            cluster_creator_task = EmrCreateJobFlowOperator(
                task_id='create_job_flow',
                job_flow_overrides=JOB_FLOW_OVERRIDES,
                region_name=REGION_NAME
            )
            job_flow_id = f"{{{{ task_instance.xcom_pull(task_ids='{task_id}.create_job_flow', key='return_value') }}}}"

        # adicionar steps ao cluster
        add_debug_step_task = EmrAddStepsOperator(
            task_id='add_debug_steps',
            job_flow_id=job_flow_id,
            aws_conn_id='aws_default',
            steps=__generate_emr_steps(name='Setup Debugging', action_on_failure='TERMINATE_CLUSTER', args=['state-pusher-script']),
        )

        spark_steps_tasks = list()
        for i, spark_job_path in enumerate(spark_job_paths):
            file_name = spark_job_path.replace('/', '-')
            S3_KEY = f'dags/jobs/{spark_job_path}'
            S3_URI = f's3://{S3_BUCKET}/{S3_KEY}'

            run_args = ['spark-submit',
                        '--master', 'yarn',
                        '--deploy-mode', 'cluster',
                        '--py-files', f's3://cortex-data-platform-mwaa-{ENVIRONMENT}/dependencies.zip',
                        S3_URI]
            if jobs_kwargs is not None:
                for k, v in jobs_kwargs.items():
                    run_args.append(k)
                    run_args.append(v)

            add_job_step_task = EmrAddStepsOperator(
                task_id=f'add_steps_{file_name}',
                job_flow_id=job_flow_id,
                aws_conn_id='aws_default',
                steps=__generate_emr_steps(name=f'Run Spark Job - {file_name}', args=run_args),
                retries=retries,
                retry_delay=60
            )

            step_checker_task = EmrStepSensor(
                task_id=f'watch_step_{file_name}',
                job_flow_id=job_flow_id,
                step_id=f"{{{{ task_instance.xcom_pull(task_ids='{add_job_step_task.task_id}', key='return_value')[-1] }}}}",
                aws_conn_id='aws_default',
                retries=retries,
                retry_delay=60
            )

            spark_steps_tasks.append(add_job_step_task)
            add_job_step_task >> step_checker_task
            if i > 0:
                spark_steps_tasks[i-1] >> add_job_step_task

        cluster_creator_task >> add_debug_step_task >> spark_steps_tasks[0]

    return emr_task_group
