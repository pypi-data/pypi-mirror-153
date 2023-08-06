from abc import ABCMeta
from abc import abstractmethod
from typing import Dict

from broccoli_server.content import ContentStore


class ApiHandler(metaclass=ABCMeta):
    @abstractmethod
    def handle_request(
        self, path: str, query_params: Dict, content_store: ContentStore
    ):
        pass
