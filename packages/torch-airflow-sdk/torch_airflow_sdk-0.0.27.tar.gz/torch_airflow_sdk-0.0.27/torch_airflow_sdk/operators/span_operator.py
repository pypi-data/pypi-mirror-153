from datetime import datetime
from airflow.models.baseoperator import BaseOperator
from torch_airflow_sdk.utils.torch_client import TorchDAGClient
from torch_sdk.events.generic_event import GenericEvent

import logging

LOGGER = logging.getLogger("airflow.task")


class SpanOperator(BaseOperator):
    """
    Description:
        Used to send span start and end event for any std airflow operator. Just wrap your operator with span operator.
        Make sure you do not add your task in dag. If you wrap it using span operator, will take care of that task operator.

    You need to add extra parameter mentioned below. Other parameters will be same as std airflow base operator's parameters

    :param operator: std task operator defined
    :param pipeline_uid: uid of the pipeline
    :param span_uid: span uid for the task
    :param associated_job_uids: list of job uids
    :param xcom_to_event_mapper_ids: list of xcom keys. Used to send xcom variables in span event job

    """
    def __init__(self, *, operator: BaseOperator, pipeline_uid=None, span_uid: str = None, associated_job_uids = None, xcom_to_event_mapper_ids= None, **kwargs):
        """
        You need to add extra parameter mentioned below. Other parameters will be same as std airflow base operator's parameters
        :param operator: std task operator defined
        :param pipeline_uid: uid of the pipeline
        :param span_uid: span uid for the task
        :param associated_job_uids: list of job uids
        :param xcom_to_event_mapper_ids: list of xcom keys. Used to send xcom variables in span event
        Example :

        --> Defined std operator.

        postgres_operator = PostgresOperator(
            task_id="task_name",
            postgres_conn_id='example_db',
            sql="select * from information_schema.attributess",
        )


        --> To wrap operator with span. Write assign this to your dag (not your std operator)

        span_operator = SpanOperator(
            task_id='task_name',
            pipeline_uid='pipeline.uid',
            span_uid='span.uid',
            operator=postgres_operator,
            dag=dag
        )

        """
        if kwargs.get("provide_context"):
            kwargs.pop('provide_context', None)
        super().__init__(**kwargs)
        self.operator = operator
        self.pipeline_uid = pipeline_uid
        self.span_uid = span_uid
        self.pipeline_run = None
        if associated_job_uids is None:
            self.associated_job_uids = []
        else:
            self.associated_job_uids = associated_job_uids
        self.xcom_to_event_mapper_ids = xcom_to_event_mapper_ids

    def execute(self, context):
        try:
            LOGGER.info("Send span start event")
            task_instance = context['ti']
            parent_span_context = task_instance.xcom_pull(key='parent_span_context')
            if parent_span_context is None:
                LOGGER.debug('sending new request to catalog to get parent span context')
                client = TorchDAGClient()
                self.pipeline_run = client.get_parent_span(pipeline_uid=self.pipeline_uid,
                                                           parent_span_uid=f'{self.pipeline_uid}.span')
                # task_instance.xcom_push(key="parent_span_context", value=self.pipeline_run.__dict__)
            else:
                LOGGER.debug('using xcom to get parent span context to send span event')
                self.pipeline_run = parent_span_context
            self.span_context = self.pipeline_run.create_child_span(uid=self.span_uid,
                                                                    context_data={'time': str(datetime.now())},
                                                                    associatedJobUids= self.associated_job_uids
                                                                    )
            context['span_context_parent'] = self.span_context
            xcom_context_data = {}
            if self.xcom_to_event_mapper_ids is None:
                self.xcom_to_event_mapper_ids = []
            else:
                for key in self.xcom_to_event_mapper_ids:
                    value = task_instance.xcom_pull(key=key)
                    if value is not None:
                        xcom_context_data[key] = value
            try:
                self.operator.prepare_for_execution().execute(context)
            except Exception as e1:
                if type(e1) == AttributeError:
                    try:
                        self.operator.execute(context)
                    except Exception as e2:
                        LOGGER.error(e2)
                        raise e2
                else:
                    LOGGER.error(e1)
                    raise e1
        except Exception as e:
            LOGGER.error("Send span end failure event")
            exception = e.__dict__
            LOGGER.error(exception)
            self.span_context.send_event(
                GenericEvent(context_data={'status': 'error', 'error_data': str(e), 'time': str(datetime.now()),
                                           'exception_type': str(type(e).__name__)},
                             event_uid=f'{self.span_uid}.error.event'))
            self.span_context.failed(
                context_data=xcom_context_data)
            raise e
        else:
            LOGGER.info("Send span end success event")
            self.span_context.end(context_data=xcom_context_data)

    def set_downstream(self, task_or_task_list) -> None:
        super().set_downstream(task_or_task_list)

    def set_upstream(self, task_or_task_list) -> None:
        super().set_upstream(task_or_task_list)
