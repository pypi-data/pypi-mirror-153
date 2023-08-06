import json
import logging
from typing import Dict

from .base import Backend


class DummyBackend(Backend):
    def __init__(self, backend_kwargs: Dict):
        super(DummyBackend, self).__init__(backend_kwargs)

    def send(self, partition: str, data: Dict):
        logging.info(
            "<{%s}> PARTITION: %s; DATA: %s", self, partition, json.dumps(data)
        )
