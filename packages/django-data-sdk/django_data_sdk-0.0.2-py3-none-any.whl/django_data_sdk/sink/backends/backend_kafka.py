import json
from typing import Dict

from kafka import KafkaProducer

from .base import Backend


class KafkaBackend(Backend):
    def __init__(self, backend_kwargs: Dict):
        super(KafkaBackend, self).__init__(backend_kwargs)
        self.producer = KafkaProducer(**self.backend_kwargs)

    def send(self, partition: str, data: Dict):
        encoded_data = json.dumps(data).encode("utf-8")
        self.producer.send(partition, encoded_data)
