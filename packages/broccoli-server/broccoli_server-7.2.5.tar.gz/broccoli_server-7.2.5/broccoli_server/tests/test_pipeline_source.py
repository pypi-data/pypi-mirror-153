from typing import Dict, List

from broccoli_server.interface.worker import WorkContext
from broccoli_server.pipeline import PipelineSource
from broccoli_server.worker.work_context import WorkContextImpl

from .testcase_with_mongomock import TestCaseWithMongoMock


class TestPipelineSource(TestCaseWithMongoMock):
    def test_successful_process(self):
        source_id = "demo_source"

        class Source(PipelineSource):
            def __init__(self, idempotency_key: str, starting_state: str):
                super().__init__(idempotency_key, starting_state)
                self.post_process_run = False

            def process(self, context: WorkContext) -> List[Dict]:
                return [{"attr1": "a"}, {"attr1": "b"}]

            def post_process(
                self, context: WorkContext, processed_documents: List[Dict]
            ):
                # TODO: would be ideal if it sets something in metadata store, but couldn't set that up :(
                self.post_process_run = True

            def get_id(self) -> str:
                return source_id

            def pre_work(self, context: WorkContext):
                pass

        demo_work_context = WorkContextImpl(
            source_id, self.content_store, self.metadata_store_factory
        )
        source = Source("attr1", "state1")
        source.work(demo_work_context)
        assert self.actual_documents_without_id() == [
            {"attr1": "a", "_state": "state1"},
            {"attr1": "b", "_state": "state1"},
        ]
        assert source.post_process_run
