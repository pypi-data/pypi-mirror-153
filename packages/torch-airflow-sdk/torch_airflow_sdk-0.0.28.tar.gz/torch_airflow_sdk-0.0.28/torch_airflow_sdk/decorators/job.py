import functools
import logging
from torch_sdk.models.job import CreateJob, JobMetadata, Dataset
from torch_airflow_sdk.utils.torch_client import TorchDAGClient
from datetime import datetime

LOGGER = logging.getLogger("airflow.task")


def job(job_uid, pipeline_uid, inputs=[], outputs=[], metadata=None):
    """
    Description:
        Used to create functional node (job) in your pipeline. Just decorate your function with `job` annotation
    :param job_uid: job uid of the pipeline
    :param pipeline_uid: uid of the pipeline
    :param inputs: input arrays of the task
    :param outputs: output array of the job
    :param metadata: metadata of the job

    Example:

    from torch_sdk.models.job import JobMetadata, Dataset

    @job(job_uid='customer.order.join.job',
        pipeline_uid='customer.orders.monthly.agg.demo',
        inputs=[Dataset('POSTGRES_LOCAL_DS', 'pipeline.pipeline.orders'), Dataset('POSTGRES_LOCAL_DS', 'pipeline.pipeline.customers')] ,
        outputs=[Dataset('POSTGRES_LOCAL_DS', 'pipeline.pipeline.customer_orders')],
        metadata=JobMetadata('name', 'team', 'code_location')
    )

    def function(**context)
    """
    def decorator_job(func):
        @functools.wraps(func)
        def wrapper_job(*args, **kwargs):
            try:
                LOGGER.info("Creating job.")
                client = TorchDAGClient()
                pipeline = client.get_pipeline(pipeline_uid)
                job = CreateJob(
                    uid=job_uid,
                    name=f'{job_uid} Job',
                    pipelineSnapshot=pipeline.currentSnapshot,
                    description=f'{job_uid} created using torch job decorator',
                    inputs=inputs,
                    outputs=outputs,
                    meta=metadata,
                    context={'job': 'torch_job_decorator', 'time': str(datetime.now()), 'uid': job_uid,
                             'function': str(func)}
                )
                job = pipeline.create_job(job)
                func(*args, **kwargs)
            except Exception as e:
                LOGGER.error("Error in creating job")
                exception = e.__dict__
                LOGGER.error(exception)
                raise e
            else:
                LOGGER.info("Successfully created job.")

        return wrapper_job

    return decorator_job
