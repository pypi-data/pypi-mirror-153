from typing import Dict


class Backend:
    def __init__(self, backend_kwargs: Dict):
        self.backend_kwargs = backend_kwargs

    def send(self, partition: str, data: Dict):
        raise NotImplementedError
