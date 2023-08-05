import functools

import logging

from torch_airflow_sdk.utils.callback import on_dag_success_callback, on_dag_failure_callback

LOGGER = logging.getLogger("airflow.task")


def handle_dag_callback(func):
    """
    Used to decorate callback function in side torch dag implementation.
    :param func: function to decorate
    """
    @functools.wraps(func)
    def wrapper_callback(*args, **kwargs):
        try:
            LOGGER.info("Decorator callback - start")
            context = None
            if len(args) > 0:
                context = args[0]
            if context is not None:
                if context['reason'] == 'success':
                    on_dag_success_callback(context=context)
                else:
                    on_dag_failure_callback(context=context)
            func(*args, **kwargs)
        except Exception as e:
            LOGGER.error("Decorator callback failed")
            exception = e.__dict__
            LOGGER.error(exception)
            raise e
        else:
            LOGGER.info("Decorator callback - end")

    return wrapper_callback
