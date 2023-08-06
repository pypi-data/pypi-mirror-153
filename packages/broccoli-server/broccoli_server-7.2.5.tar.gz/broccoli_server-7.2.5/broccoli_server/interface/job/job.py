from abc import ABCMeta
from abc import abstractmethod

from .job_context import JobContext


class Job(metaclass=ABCMeta):
    @abstractmethod
    def work(self, context: JobContext):
        pass
