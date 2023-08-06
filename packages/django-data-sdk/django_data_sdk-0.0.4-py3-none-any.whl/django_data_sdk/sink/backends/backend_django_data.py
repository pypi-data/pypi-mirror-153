import json
import logging
from typing import Dict

from .base import Backend


class DjangoDataBackend(Backend):
    def send(self, partition: str, data: Dict):
        logging.info(
            "<{%s}> PARTITION: %s; DATA: %s", self, partition, json.dumps(data)
        )
