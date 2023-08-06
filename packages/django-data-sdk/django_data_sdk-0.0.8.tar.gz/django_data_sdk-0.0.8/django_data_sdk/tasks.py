import logging
from typing import Dict, Optional

from celery import shared_task
from django_data_sdk.conf.settings import DJANGO_DATA_SINK_SETTINGS
from django_data_sdk.sink.backends.base import Backend
from django_data_sdk.sink.utils import get_backend_instance


BACKEND_INSTANCE: Optional[Backend] = None


def ensure_backend_instance():
    global BACKEND_INSTANCE
    if BACKEND_INSTANCE:
        return BACKEND_INSTANCE
    backend = DJANGO_DATA_SINK_SETTINGS["backend"]
    backend_kwargs = DJANGO_DATA_SINK_SETTINGS["backend_kwargs"]
    BACKEND_INSTANCE = get_backend_instance(backend, backend_kwargs)
    return get_backend_instance(backend, backend_kwargs)


@shared_task()
def send_data_task(*, partition: str, data: Dict):
    backend_instance = ensure_backend_instance()
    try:
        backend_instance.send(partition, data)
    except Exception as e:
        logging.error("error when send data to sink backend", exc_info=e)
        # force a re-initialization of backend instance
        global BACKEND_INSTANCE
        BACKEND_INSTANCE = None
        # use celery's retry function
        raise e
