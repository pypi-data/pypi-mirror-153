import datetime
import logging
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Optional

from django_data_sdk.conf.settings import DJANGO_DATA_SINK_THREAD_POOL_SIZE
from django_data_sdk.sink import mode
from django_data_sdk.sink.backends.base import Backend
from django_data_sdk.sink.utils import get_backend_instance
from django_data_sdk.tasks import send_data_task


class Sink:
    SINK_POOL = ThreadPoolExecutor(max_workers=DJANGO_DATA_SINK_THREAD_POOL_SIZE)
    SINK_INSTANCE = None

    @classmethod
    def get_sink_instance(cls, sink_settings) -> "Sink":
        if cls.SINK_INSTANCE is None:
            cls.SINK_INSTANCE = Sink(**sink_settings)
        return cls.SINK_INSTANCE

    def __init__(
        self,
        backend: str,
        backend_kwargs: Dict,
        partition_prefix: str,
        partition_by: str,
        partition_date_format: str,
        app_secret: str,
        sink_mode: str = mode.DIRECT,
    ):
        self.sink_backend = backend
        self.sink_backend_kwargs = backend_kwargs
        self.partition_prefix = partition_prefix
        self.partition_by = partition_by
        self.partition_date_format = partition_date_format
        self.app_secret = app_secret
        self.sink_mode = sink_mode

        self._backend_instance: Optional[Backend] = None
        self._send_data_task = None
        self._put_method = None

    def _ensure_backend_and_put_method(self):
        if self.sink_mode == mode.DIRECT:
            self._backend_instance = get_backend_instance(
                self.sink_backend, self.sink_backend_kwargs
            )
            self._put_method = self.put_direct
        elif self.sink_mode == mode.CELERY:
            self._send_data_task = send_data_task
            self._put_method = self.put_celery

    def put(self, data: Dict):
        self.SINK_POOL.submit(self._put, data)

    def _put(self, data: Dict):
        if self._put_method is None:
            try:
                self._ensure_backend_and_put_method()
            except Exception as e:
                logging.error(
                    "failed to initialize sink backend and put_method on the fly",
                    exc_info=e,
                )
                return
            else:
                logging.info(
                    "initialize sink backend and put_method successfully on the fly"
                )

        try:
            partition = self._get_partition(data)
            self._put_method(partition, data)
        except Exception as e:
            self._put_method = None
            self._backend_instance = None
            logging.error("sink put error", exc_info=e)

    def put_direct(self, partition: str, data: Dict):
        # make sure self._backend_instance is initialized successfully
        if self._backend_instance:
            self._backend_instance.send(partition=partition, data=data)

    def put_celery(self, partition: str, data: Dict):
        self._send_data_task.apply_async(
            kwargs={
                "partition": partition,
                "data": data,
            }
        )

    def _get_partition(self, data: Dict) -> str:
        partition_by_value = data["context"][self.partition_by]
        partition_by = datetime.datetime.fromisoformat(partition_by_value).strftime(
            self.partition_date_format
        )
        return f"{self.partition_prefix}_{partition_by}"
