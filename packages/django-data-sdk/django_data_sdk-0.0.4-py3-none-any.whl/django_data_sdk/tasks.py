import logging
from typing import Dict

from celery import shared_task
from django_data_sdk.conf.settings import DJANGO_DATA_SINK_SETTINGS


@shared_task()
def send_data_task(*, partition: str, data: Dict):
    logging.info("task sink_data %s", data)
