from time import sleep
from airflow.operators.python_operator import PythonOperator
import psycopg2
import random
from datetime import datetime
import datetime as dt
from torch_sdk.models.job import JobMetadata, Dataset
from torch_sdk.events.generic_event import GenericEvent
import logging

LOGGER = logging.getLogger("airflow.task")
from airflow.operators.postgres_operator import PostgresOperator
from torch_airflow_sdk.decorators.job import job
from torch_airflow_sdk.decorators.span import span
from torch_airflow_sdk.dag import DAG
from torch_airflow_sdk.operators.torch_initialiser_operator import TorchInitializer
from torch_airflow_sdk.operators.span_operator import SpanOperator

default_args = {'start_date': datetime(2020, 1, 1)}


def create_customer(index):
    return "customer" + str(index)


def create_orders(customer_id):
    orders = []
    for i in range(5):
        add_months = random.randint(0, 11)
        order = {
            'customer_id': customer_id,
            'items_count': random.randint(5, 10),
            'unit_price': random.randint(10, 20),
            'created_at': datetime(2021, 1, 1) +
                          dt.timedelta(days=30 * add_months)
        }
        orders.append(order)
    return orders


def create_conn():
    return psycopg2.connect(
        host="torch.acceldata.local",
        port=5432,
        database="example",
        user="postgres",
        password="postgres")


@job(job_uid='customer.order.datagen.job',
     pipeline_uid='customer.orders.monthly.agg.demo',
     inputs=[],
     outputs=[Dataset('POSTGRES_LOCAL_DS', 'pipeline.pipeline.orders'),
              Dataset('POSTGRES_LOCAL_DS', 'pipeline.pipeline.customers')],
     metadata=JobMetadata('Vaishvik_brahmbhatt', 'backend', 'https://github.com/acme/reporting/report.scala')
     )
@span(span_uid='customer.orders.datagen.span', pipeline_uid='customer.orders.monthly.agg.demo')
def data_gen(**context):
    conn = create_conn()
    customer_sql = """INSERT INTO pipeline.customers(name) VALUES(%s) RETURNING id;"""
    orders_sql = """INSERT INTO pipeline.orders(customer_id, items_count, unit_price, created_at) VALUES(%s, %s, %s, %s) RETURNING id;"""

    datagen_span_context = context['span_context_parent']
    customer_datagen_span = datagen_span_context.create_child_span(
        uid="customer.data.gen", context_data={'client_time': str(datetime.now())})

    cur = conn.cursor()
    customer_ids = []
    print("Creating dummy customers")
    for i in range(1, 101):
        customer_name = create_customer(i)
        cur.execute(customer_sql, (customer_name,))
        customer_id = cur.fetchone()[0]
        customer_ids.append(customer_id)
    conn.commit()

    sleep(1)
    customer_datagen_span.end(
        {'client_time': str(datetime.now()), 'customers_count': len(customer_ids)})

    print("Creating dummy orders for each customers")

    orders_datagen_span = datagen_span_context.create_child_span(
        uid="order.data.gen", context_data={'client_time': str(datetime.now())})

    cur = conn.cursor()
    count = 0
    for customer_id in customer_ids:
        customer_orders = create_orders(customer_id)
        for order in customer_orders:
            cur.execute(orders_sql, (customer_id,
                                     order['items_count'], order['unit_price'], order['created_at']))
            count += 1

    cur.close()
    conn.commit()
    sleep(1)
    orders_datagen_span.end(
        {'client_time': str(datetime.now()), 'orders_count': count})
    conn.close()


@job(job_uid='customer.order.join.job',
     pipeline_uid='customer.orders.monthly.agg.demo',
     inputs=[Dataset('POSTGRES_LOCAL_DS', 'pipeline.pipeline.orders'),
             Dataset('POSTGRES_LOCAL_DS', 'pipeline.pipeline.customers')],
     outputs=[Dataset('POSTGRES_LOCAL_DS', 'pipeline.pipeline.customer_orders')],
     metadata=JobMetadata('Vaishvik_brahmbhatt', 'backend', 'https://github.com/acme/reporting/report.scala')
     )
@span(span_uid='customer.orders.join.span', pipeline_uid='customer.orders.monthly.agg.demo')
def customer_order_join(**context):
    conn = create_conn()
    join_sql = """SELECT co.id as customer_id, co.name, o.items_count * o.unit_price as total_order_value, o.created_at as ordered_at
    FROM pipeline.orders o JOIN pipeline.customers co on o.customer_id = co.id;"""
    cur = conn.cursor()
    cur.execute(join_sql)
    rows = cur.fetchall()
    cur.close()
    conn.commit()
    conn.close()

    join_span_context = context['span_context_parent']
    join_span_context.send_event(GenericEvent(context_data={'client_time': str(datetime.now()), 'row_count': len(rows)},
                                              event_uid="order.customer.join.result"))

    task_instance = context['ti']
    task_instance.xcom_push(key="rows", value=rows)


@span(span_uid='customer.orders.insert.span', pipeline_uid='customer.orders.monthly.agg.demo')
def customer_order_gen(**context):
    conn = create_conn()
    insert_sql = """INSERT INTO pipeline.customer_orders(customer_id, customer_name, total_order_value, ordered_at)
             VALUES(%s, %s, %s, %s) RETURNING id;"""
    print("Inserting joined record into the orders table")
    cur = conn.cursor()
    task_instance = context['ti']
    rows = task_instance.xcom_pull(key="rows")
    for row in rows:
        cur.execute(insert_sql, (row[0], row[1], row[2], row[3]))
    cur.close()
    conn.commit()
    sleep(1)
    conn.close()


@job(job_uid='monthly.order.aggregate.job',
     pipeline_uid='customer.orders.monthly.agg.demo',
     inputs=[Dataset('POSTGRES_LOCAL_DS', 'pipeline.pipeline.customer_orders')],
     outputs=[Dataset('POSTGRES_LOCAL_DS', 'pipeline.pipeline.customer_orders_monthly_agg')],
     metadata=JobMetadata('Vaishvik_brahmbhatt', 'backend', 'https://github.com/acme/reporting/report.scala')
     )
@span(span_uid='monthy.aggregate.span', pipeline_uid='customer.orders.monthly.agg.demo')
def monthly_order_aggregate(**context):
    conn = create_conn()
    insert_sql = """
      INSERT INTO pipeline.customer_orders_monthly_agg(customer_name, customer_id, order_month, total_order_value)
      SELECT customer_name, customer_id,EXTRACT(MONTH FROM ordered_at) as month, SUM(total_order_value)
      FROM pipeline.customer_orders GROUP BY customer_name, EXTRACT(MONTH FROM ordered_at), customer_id;
    """
    print("Aggregating the orders over months per customer")
    cur = conn.cursor()
    cur.execute(insert_sql)
    cur.close()
    conn.commit()
    sleep(1)
    conn.close()


def failure_callback(context):
    pass


def success_callback(context):
    pass


get_order_agg_for_q4 = PostgresOperator(
    task_id="get_monthly_order_aggregate_last_quarter",
    postgres_conn_id='example_db',
    sql="select * from information_schema.attributes",
)

get_order_agg_for_q1 = PostgresOperator(
    task_id="get_monthly_order_aggregate_first_quarter",
    postgres_conn_id='example_db',
    sql="select * from information_schema.attributess",
)

dag = DAG(
    dag_id='pipeline_demo_final',
    schedule_interval='@daily',
    default_args=default_args,
    start_date=datetime(2020, 2, 2),
    catchup=False,
    on_failure_callback=failure_callback,
    on_success_callback=success_callback,
    pipeline_uid='customer.orders.monthly.agg.demo'
)

torch_initializer_task = TorchInitializer(
    task_id='torch_pipeline_initializer',
    pipeline_uid='customer.orders.monthly.agg.demo',
    dag=dag
)

insert_data = PythonOperator(
    task_id='insert_data_in_customers_and_orders_table',
    python_callable=data_gen,
    provide_context=True,
    dag=dag
)

customer_orders_join = PythonOperator(
    task_id='customer_order_join',
    python_callable=customer_order_join,
    provide_context=True,
    dag=dag
)

customer_orders_gen = PythonOperator(
    task_id='customer_order_generate_n_insert',
    python_callable=customer_order_gen,
    provide_context=True,
    dag=dag
)

monthly_order_agg = PythonOperator(
    task_id='monthly_order_aggregate',
    python_callable=monthly_order_aggregate,
    provide_context=True,
    dag=dag
)

get_order_agg_for_q1 = SpanOperator(
    task_id='get_monthly_order_aggregate_first_quarter',
    pipeline_uid='customer.orders.monthly.agg.demo',
    span_uid='monthly.order.agg.q1.span',
    operator=get_order_agg_for_q1,
    dag=dag
)

torch_initializer_task >> insert_data >> customer_orders_join >> customer_orders_gen >> monthly_order_agg >> get_order_agg_for_q4 >> get_order_agg_for_q1