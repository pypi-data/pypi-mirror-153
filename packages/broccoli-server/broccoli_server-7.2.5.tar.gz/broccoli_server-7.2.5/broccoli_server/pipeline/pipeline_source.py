import abc
from typing import Dict, List

from broccoli_server.interface.worker import WorkContext
from broccoli_server.interface.worker import Worker

from .state_key import StateKey


class PipelineSource(Worker, abc.ABC):
    def __init__(self, idempotency_key: str, starting_state: str):
        self.idempotency_key = idempotency_key
        self.starting_state = starting_state

    @abc.abstractmethod
    def process(self, context: WorkContext) -> List[Dict]:
        pass

    @abc.abstractmethod
    def post_process(self, context: WorkContext, processed_documents: List[Dict]):
        pass

    def work(self, context: WorkContext):
        processing_documents = self.process(context)

        context.logger().info(
            f"Appending {len(processing_documents)} item(s) for {self.starting_state} state"
        )
        documents = []
        for d in processing_documents:
            d[StateKey] = self.starting_state
            documents.append(d)

        context.content_store().append_multiple(
            docs=documents, idempotency_key=self.idempotency_key
        )

        self.post_process(context, processing_documents)
