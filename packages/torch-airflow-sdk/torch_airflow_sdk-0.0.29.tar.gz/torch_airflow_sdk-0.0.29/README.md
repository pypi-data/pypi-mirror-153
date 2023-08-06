# TORCH-AIRFLOW-SDK
Torch airflow sdk provides support for observability of airflow dags in torch catalog. With the use of torch airflow sdk, user can e2e observability on airflow dag run in torch UI. Every dag is associated with pipeline in torch.
<br />
Make sure while configuring airflow, 3 environmental needs to be set up in airflow env.
docker container.
- TORCH_CATALOG_URL - URL of the torch catalog
- TORCH_ACCESS_KEY - API access key generated from torch UI
- TORCH_SECRET_KEY - API secret key generated from torch UI


First of all, install below mentioned 2 pypi package to expose ETL in torch.
```bash
pip install torch-sdk
```

Read more about torch-sdk from [here](https://pypi.org/project/torch-sdk/)

```bash
pip install torch-airflow-sdk
```

Read more about torch-airflow-sdk from [here](https://pypi.org/project/torch-airflow-sdk/)

## Create Pipeline
First of all, to create a pipeline in torch, the user needs to create a pipeline using torch-sdk. To know more about pipeline, check torch-sdk documentation that contains detailed information about torch pipeline usage.

```python
from torch_sdk.models.pipeline import CreatePipeline, PipelineMetadata
from torch_sdk.torch_client import TorchClient

torchClient = TorchClient(url="https://torch.acceldata.local:5443",
                       access_key="OY2VVIN2N6LJ", secret_key="da6bDBimQfXSMsyyhlPVJJfk7Zc2gs")

pipeline = CreatePipeline(
    uid='customer.orders.monthly.agg',
    name='Customer Orders Monthly aggregate',
    description='Pipeline to Aggregate the customer orders over 1 year',
    meta=PipelineMetadata(
        owner='vaishvik', team='torch', codeLocation='...'),
    context={
        'associated_tables': 'pipeline.customer, pipeline.orders, pipeline.customer_orders, pipeline.customer_orders_monthly_agg'}
)

pipeline_res = torchClient.create_pipeline(pipeline=pipeline)
```
## Create DAG
In airflow DAG code, import torch dag instead of airflow dag. All the parameters will be the same as standard apache airflow dag. But there will be one additional parameter `pipeline_uid` to map dag with the corresponding pipeline.
```python
from torch_airflow_sdk.dag import DAG
dag = DAG(
   dag_id='pipeline_demo_final',
   schedule_interval='@daily',
   default_args=default_args,
   start_date=datetime(2020, 2, 2),
   catchup=False,
   on_failure_callback= failure_callback,
   on_success_callback= success_callback,
   pipeline_uid='customer.orders.monthly.agg.demo'
)
```



## Create Job
To create a job in the pipeline, the user needs to decorate the python function with a job decorator as shown in the below example. Pass some required parameters (job uid, pipeline uid, metadata object and input-output asset list) inside the decorator. Make sure, inside a Dataset the type of the object which will have `source` (data source name inside torch catalog) and `asset_uid` (asset path from its root) as parameters.
```python
from torch_airflow_sdk.decorators.job import job
from torch_sdk.models.job import JobMetadata, Dataset
@job(job_uid='monthly.order.aggregate.job',
   pipeline_uid='customer.orders.monthly.agg.demo',
   inputs=[Dataset('POSTGRES_LOCAL_DS', 'pipeline.pipeline.customer_orders')],
   outputs=[Dataset('POSTGRES_LOCAL_DS', 'pipeline.pipeline.customer_orders_monthly_agg')],
   metadata=JobMetadata(name = 'Vaishvik_brahmbhatt', team = 'backend', code_location ='https://github.com/acme/reporting/report.scala')
   )
def monthly_order_aggregate(**context):
    pass
```


## Create Span Using Decorator
To create a span for a python function, the user can decorate a python function with a span decorator that contains span uid and pipeline uid as parameters. To decorate function with span make sure, it has `**context` parameter inside the function argument. That gives access to the context of the task. Using the context, various span events can be sent inside the function.  To get the parent span context, use the key name `span_context_parent` in xcom pull of the task instance. It’s value will be span context instance which can  be used to create child spans and send custom events (As shown in below example.)
```python
from torch_airflow_sdk.decorators.span import span
from torch_sdk.events.generic_event import GenericEvent
@span(span_uid='customer.orders.datagen.span', pipeline_uid='customer.orders.monthly.agg.demo',
      associated_job_uids = ['monthly.order.aggregate.transfer'],  xcom_to_event_mapper_ids = ['run_id', 'event_id'] )
def data_gen(**context):
   datagen_span_context = context['span_context_parent']
   customer_datagen_span = datagen_span_context.create_child_span(
       uid="customer.data.gen", 
      context_data= {'client_time': str(datetime.now()) }
   )
   customer_datagen_span.send_event(
      GenericEvent(
         context_data={
            'client_time': str(datetime.now()), 
            'row_count': len(rows)
         }, 
         event_uid="order.customer.join.result"
      )
   )
   customer_datagen_span.end(
       context_data={'client_time': str(datetime.now()), 'customers_count': len(customer_ids) }
   )

```


## Custom Operators 
Torch airflow sdk contains 2 custom operators. 
#####TorchInitializer Operator : 
In airflow `2.0` , the user needs to add a task with a given operator at the root of your dag. This will create new pipeline
run for the each dag run of the airflow dag. In airflow `1.0`, it's not needed. It’s taken care of inside torch airflow sdk. But for `2.0`, the user needs to add it as a root of the dag. This is because of the DAG serialization feature added in it to reduce load on the web server and scheduler side in airflow. To fulfill that requirement, additional parameters need to be added at the root of the DAG in case of airflow `2.0`.
```python
from torch_airflow_sdk.operators.torch_initialiser_operator import TorchInitializer

torch_initializer_task = TorchInitializer(
   task_id='torch_pipeline_initializer',
   pipeline_uid='customer.orders.monthly.agg.demo',
   pipeline_name='CUSTOMERS ORDERS MOTHLY AGG',
   dag=dag
)

```
##### SpanOperator Operator : 
Span operator used to send span start and end the event for any std airflow operator. Just wrap the std operator with a span operator.
Make sure that the wrapped operator should not be added in the DAg. If the operator is wrapped with a span operator, the span operator will take care of that task operator inside its execution. It will have some required parameters ( `span_uid` : uid of the span, `pipeline_uid` : uid of the pipeline , `operator` : standard operator task that needs to be wrapped with span ). Other parameters will be the same as the airflow standard base operator. 
 ```python
from torch_airflow_sdk.operators.span_operator import SpanOperator

get_order_agg_for_q4 = PostgresOperator(
   task_id="get_monthly_order_aggregate_last_quarter",
   postgres_conn_id='example_db',
   sql="select * from information_schema.attributess",
)

get_order_agg_for_q4 = SpanOperator(
   task_id="get_monthly_order_aggregate_last_quarter",
   pipeline_uid='customer.orders.monthly.agg.demo',
   span_uid='monthly.order.agg.q4.span',
   operator=get_order_agg_for_q4,
   associated_job_uids = ['monthly.order.aggregate.transfer'],  
   xcom_to_event_mapper_ids = ['run_id', 'event_id'] ,
   dag=dag
)
```