from abc import ABCMeta
from abc import abstractmethod
import logging
from typing import List

from broccoli_server.content import ContentStore


class JobContext(metaclass=ABCMeta):
    @abstractmethod
    def logger(self) -> logging.Logger:
        pass

    @abstractmethod
    def content_store(self) -> ContentStore:
        pass

    @abstractmethod
    def drain_log_lines(self) -> List[str]:
        pass
