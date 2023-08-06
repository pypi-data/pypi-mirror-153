from airflow import DAG
from airflow.utils.log.logging_mixin import LoggingMixin
from torch_airflow_sdk.decorators.handle_callback import handle_dag_callback
from torch_airflow_sdk.utils.callback import on_dag_success_callback, on_dag_failure_callback
from torch_airflow_sdk.utils.torch_client import TorchDAGClient


class DAG(DAG, LoggingMixin):
    """
    Description:
        DAG Wrapper created by torch. To observe airflow ETL in torch UI.
    A dag (directed acyclic graph) is a collection of tasks with directional
    dependencies. A dag also has a schedule, a start date and an end date
    (optional). For each schedule, (say daily or hourly), the DAG needs to run
    each individual tasks as their dependencies are met. Certain tasks have
    the property of depending on their own past, meaning that they can't run
    until their previous schedule (and upstream tasks) are completed.

    DAGs essentially act as namespaces for tasks. A task_id can only be
    added once to a DAG.

    To create DAG, you need to pass one additional parameter pipeline_uid. Other parameters will be same as standard apache airflow DAG.

    """
    def __init__(self, pipeline_uid, *args, **kwargs):
        """
            Description:
            To create DAG, you need to pass one additional parameter pipeline_uid. Other parameters will be same as standard apache airflow DAG.
        :param pipeline_uid: (String) uid of the pipeline given in torch

        """
        self.pipeline_uid = pipeline_uid
        success_callback_func = on_dag_success_callback
        failure_callback_func = on_dag_failure_callback
        is_override_failure_callback = kwargs.get('override_failure_callback', False)
        kwargs.pop('override_failure_callback')
        is_override_success_callback = kwargs.get('override_success_callback', False)
        kwargs.pop('override_success_callback')
        if 'on_failure_callback' in kwargs:
            if not is_override_failure_callback:
                # If callback is provided and override is False then use both callbacks
                failure_callback_func = handle_dag_callback(kwargs['on_failure_callback'])
            else:
                # If callback is provided and override is True then only customer provided callback is used
                failure_callback_func = kwargs['on_failure_callback']
            kwargs.pop('on_failure_callback')
        else:
            if is_override_failure_callback:
                # If callback is not provided but override is True then make callback NO-OP
                failure_callback_func = self.empty_failure_callback

        if 'on_success_callback' in kwargs:
            if not is_override_success_callback:
                # If callback is provided and override is False then use both callbacks
                success_callback_func = handle_dag_callback(kwargs['on_success_callback'])
            else:
                # If callback is provided and override is True then only customer provided callback is used
                success_callback_func = kwargs['on_success_callback']
            kwargs.pop('on_success_callback')
        else:
            if is_override_success_callback:
                # If callback is not provided but override is True then make callback NO-OP
                success_callback_func = self.empty_success_callback

        super(DAG, self).__init__(
            on_failure_callback=failure_callback_func,
            on_success_callback=success_callback_func,
            *args, **kwargs)

    def create_dagrun(self, *args, **kwargs):
        """
        Creates a dag run from this dag including the tasks associated with this dag.
        Returns the dag run.

        :return: dagrun instance
        """
        client = TorchDAGClient()
        pipeline_run = client.create_pipeline_run(self.pipeline_uid)
        pipeline_run.create_span(uid= f'{self.pipeline_uid}.span' )
        dagrun = super(DAG, self).create_dagrun(*args, **kwargs)
        return dagrun

    def empty_success_callback(self, context):
        pass

    def empty_failure_callback(self, context):
        pass
