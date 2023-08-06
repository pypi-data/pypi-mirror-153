import logging
from datetime import datetime

from airflow.operators.python_operator import PythonOperator
from torch_sdk.events.generic_event import GenericEvent
from torch_sdk.models.job import JobMetadata, Dataset

LOGGER = logging.getLogger("airflow.task")
from torch_airflow_sdk.decorators.job import job
from torch_airflow_sdk.decorators.span import span
from torch_airflow_sdk.dag import DAG
from torch_airflow_sdk.operators.torch_initialiser_operator import TorchInitializer

default_args = {'start_date': datetime(2020, 1, 1)}

etl_pipeline_uid = 'SIMPLE.DAG.ETL.NEW'
snowflake_datasource = 'SNOWFLAKE_FINANCE'


@job(job_uid='etl.job.generation',
     pipeline_uid=etl_pipeline_uid,
     inputs=[],
     outputs=[Dataset(snowflake_datasource, 'FINANCE.FINANCE.ACCELDATA_CUSTOMERS')],
     metadata=JobMetadata('Ashwin', 'TORCH', 'https://www.acceldata.io')
     )
@span(span_uid='etl.data.generation', pipeline_uid=etl_pipeline_uid,
      associated_job_uids=['etl.job.generation'])
def regional_customers_data_generation(**context):
    datagen_span_context = context['span_context_parent']
    datagen_span_context.send_event(GenericEvent(
        context_data={'client_time': str(datetime.now()), 'Total_table_to_be_generated': 1,
                      'Sync_database_type': 'SNOWFLAKE',
                      'purpose': 'Acceldata Customers data generation and filter customers by its region. (Specially INDIA)'},
        event_uid="acceldata.global.customers.metadata"))
    customer_span = datagen_span_context.create_child_span(
        uid="etl.data.creation", context_data={'client_time': str(datetime.now())})

    customer_span.send_event(GenericEvent(
        context_data={'client_time': str(datetime.now()), 'Time_taken_in_seconds': 10,
                      'New_data_generated': 100},
        event_uid="acceldata.global.customers.data.creation.metadata"))
    customer_span.end(
        {'client_time': str(datetime.now()), 'customers_count': 100})

    customers_insert_span = datagen_span_context.create_child_span(
        uid="acceldata.global.customers.data.insertion", context_data={'client_time': str(datetime.now())})

    customers_insert_span.send_event(GenericEvent(
        context_data={'client_time': str(datetime.now()), 'Total_time_taken_in_seconds': 10,
                      'Regions': ['EUROPE', 'INDIA', 'USA'],
                      'Table': ['ACCELDATA_CUSTOMERS'], 'DATA_INSERTED': 100},
        event_uid="etl.data.insertion"))
    customers_insert_span.end(
        {'client_time': str(datetime.now())})


dag = DAG(
    dag_id='TEST_DAG',
    schedule_interval='@daily',
    default_args=default_args,
    start_date=datetime(2020, 2, 2),
    catchup=False,
    pipeline_uid=etl_pipeline_uid
)

torch_initializer_task = TorchInitializer(
    task_id='torch_pipeline_initializer',
    pipeline_uid=etl_pipeline_uid,
    pipeline_name='TORCH SIMPLE DAG - NEW',
    dag=dag
)

data_gen_task = PythonOperator(
    task_id='regional_customers_data_gen',
    python_callable=regional_customers_data_generation,
    provide_context=True,
    dag=dag
)

torch_initializer_task >> data_gen_task
