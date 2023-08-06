import datetime
from airflow.operators.postgres_operator import PostgresOperator
from torch_airflow_sdk.dag import DAG
from torch_airflow_sdk.operators.torch_initialiser_operator import TorchInitializer
from torch_airflow_sdk.operators.span_operator import SpanOperator

default_args = {
    'owner': 'airflow'
}

create_emp_table = PostgresOperator(
    task_id="create_emp_table",
    postgres_conn_id='example_db',
    sql="""
        CREATE TABLE IF NOT EXISTS employee (
        emp_id SERIAL PRIMARY KEY,
        name VARCHAR NOT NULL,
        emp_type VARCHAR NOT NULL,
        birth_date DATE NOT NULL,
        company VARCHAR NOT NULL);
        """,
)
populate_emp_table = PostgresOperator(
    task_id="populate_emp_table",
    postgres_conn_id='example_db',
    sql="""
        INSERT INTO  employee( "name", emp_type, birth_date, company) VALUES ( 'Paul', 'SDE', '2018-07-05', 'amazon');
        INSERT INTO  employee( "name", emp_type, birth_date, company) VALUES ( 'Susie', 'MANAGER', '2019-05-01', 'microsoft');
        INSERT INTO  employee( "name", emp_type, birth_date, company) VALUES ( 'Lester', 'TALENT TEAM', '2020-06-23', 'block-ford');
        INSERT INTO  employee( "name", emp_type, birth_date, company) VALUES ( 'Quincy', 'HR', '2013-08-11', 'rockman');
        """,
)

get_emps = PostgresOperator(
    task_id="get_emps",
    postgres_conn_id='example_db',
    sql="SELECT * FROM employee;"
)

insert_emps = PostgresOperator(
    task_id="insert_into_empployee_table",
    postgres_conn_id='example_db',
    sql="""
        INSERT INTO  employee( "name", emp_type, birth_date, company) VALUES ( 'Vaishvik', 'SDE', '2018-07-05', 'Acceldata');
    """
)

get_emps_new = PostgresOperator(
    task_id="get_ad_emps",
    postgres_conn_id='example_db',
    sql="SELECT * FROM employee;"
)

dag = DAG(
    dag_id="torch_pkg_dag_test",
    start_date=datetime.datetime(2020, 2, 2),
    schedule_interval="@once",
    default_args=default_args,
    catchup=False,
    pipeline_uid='monthly_reporting_airflow'
)

torch_initializer_task = TorchInitializer(
    task_id='torch_pipeline_initializer',
    pipeline_uid='monthly_reporting_airflow',
    dag=dag
)

create_emp_table = SpanOperator(
    task_id='create_emp_table',
    pipeline_uid='monthly_reporting_airflow',
    span_uid='create.emps.span',
    operator=create_emp_table,
    dag=dag
)

populate_emp_table = SpanOperator(
    task_id='populate_emp_table',
    pipeline_uid='monthly_reporting_airflow',
    span_uid='populate.emps.span',
    operator=populate_emp_table,
    dag=dag
)

get_emps = SpanOperator(
    task_id='get_emps',
    pipeline_uid='monthly_reporting_airflow',
    span_uid='get.emps.span',
    operator=get_emps,
    dag=dag
)

insert_emps = SpanOperator(
    task_id='insert_emps',
    pipeline_uid='monthly_reporting_airflow',
    span_uid='insert.emps.span',
    operator=insert_emps,
    dag=dag
)

get_emps_new = SpanOperator(
    task_id='get_emps_new_acceldata',
    pipeline_uid='monthly_reporting_airflow',
    span_uid='get.emps.new.span',
    operator=get_emps_new,
    dag=dag
)

torch_initializer_task >> create_emp_table >> populate_emp_table >> get_emps >> insert_emps >> get_emps_new