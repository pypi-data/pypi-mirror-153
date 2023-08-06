from typing import Set

from broccoli_server.pipeline import Pipeline
from broccoli_server.pipeline import PipelineModView
from broccoli_server.pipeline import PipelineModViewToState
from broccoli_server.pipeline import PipelineState
from broccoli_server.pipeline import PipelineWorker

from .testcase_with_mongomock import TestCaseWithMongoMock


class TestPipeline(TestCaseWithMongoMock):
    @staticmethod
    def create_demo_worker_instance(from_state: str, to_states: Set[str]):
        return PipelineWorker(
            name="demo",
            process=lambda _: [],
            from_state=from_state,
            to_states=to_states,
        )


class TestPipelineAssertDag(TestPipeline):
    def test_assert_dag_straight_line_pipeline(self):
        pipeline = Pipeline("straight_line")
        pipeline.add_state(PipelineState("state1", {}), is_starting=True)
        pipeline.add_state(PipelineState("state2", {}))
        pipeline.add_state(PipelineState("state3", {}))
        pipeline.add_worker(self.create_demo_worker_instance("state1", {"state2"}))
        pipeline.add_mod_view(
            PipelineModView(
                "2to3", "state2", [PipelineModViewToState("state3", "state3")], [], ""
            )
        )
        pipeline.assert_pipeline_is_dag()

    def test_assert_dag_simple_pipeline(self):
        pipeline = Pipeline("simple")
        pipeline.add_state(PipelineState("state1", {}), is_starting=True)
        pipeline.add_state(PipelineState("state2", {}))
        pipeline.add_state(PipelineState("state3", {}))
        pipeline.add_state(PipelineState("state4", {}))
        pipeline.add_state(PipelineState("state5", {}))
        pipeline.add_worker(self.create_demo_worker_instance("state1", {"state2"}))
        pipeline.add_worker(self.create_demo_worker_instance("state2", {"state3"}))
        pipeline.add_worker(self.create_demo_worker_instance("state2", {"state4"}))
        pipeline.add_worker(self.create_demo_worker_instance("state3", {"state4"}))
        pipeline.add_worker(self.create_demo_worker_instance("state4", {"state5"}))
        pipeline.assert_pipeline_is_dag()

    def test_assert_not_dag(self):
        pipeline = Pipeline("not_dag")
        pipeline.add_state(PipelineState("state1", {}), is_starting=True)
        pipeline.add_state(PipelineState("state2", {}))
        pipeline.add_state(PipelineState("state3", {}))
        pipeline.add_state(PipelineState("state4", {}))
        pipeline.add_state(PipelineState("state5", {}))
        pipeline.add_worker(self.create_demo_worker_instance("state1", {"state2"}))
        pipeline.add_worker(self.create_demo_worker_instance("state3", {"state2"}))
        pipeline.add_worker(self.create_demo_worker_instance("state2", {"state4"}))
        pipeline.add_worker(self.create_demo_worker_instance("state4", {"state3"}))
        pipeline.add_worker(self.create_demo_worker_instance("state4", {"state5"}))
        self.assertRaisesRegex(
            RuntimeError, "has a cycle", pipeline.assert_pipeline_is_dag
        )

    def test_assert_missing_starting_state(self):
        pipeline = Pipeline("not_dag")
        pipeline.add_state(PipelineState("state1", {}))
        pipeline.add_state(PipelineState("state2", {}))
        pipeline.add_state(PipelineState("state3", {}))
        pipeline.add_worker(self.create_demo_worker_instance("state1", {"state2"}))
        pipeline.add_mod_view(
            PipelineModView(
                "2to3", "state2", [PipelineModViewToState("state3", "state3")], [], ""
            )
        )
        self.assertRaisesRegex(
            RuntimeError, "starting state", pipeline.assert_pipeline_is_dag
        )

    def test_assert_undiscovered_states(self):
        pipeline = Pipeline("not_dag")
        pipeline.add_state(PipelineState("state1", {}), is_starting=True)
        pipeline.add_state(PipelineState("state2", {}))
        pipeline.add_state(PipelineState("state3", {}))
        pipeline.add_state(PipelineState("state4", {}))
        pipeline.add_worker(self.create_demo_worker_instance("state1", {"state2"}))
        pipeline.add_mod_view(
            PipelineModView(
                "2to3", "state2", [PipelineModViewToState("state3", "state3")], [], ""
            )
        )
        self.assertRaisesRegex(
            RuntimeError, "undiscovered", pipeline.assert_pipeline_is_dag
        )


class TestPipelineAssertValidMigration(TestPipeline):
    def test_assert_valid_migration(self):
        pipeline = Pipeline("demo")
        pipeline.add_state(PipelineState("state1", {"attr1": True}), is_starting=True)
        pipeline.add_state(PipelineState("state2", {"attr2": True}))
        pipeline.add_state(PipelineState("state3", {"attr3": True}))
        self.content_store.append_multiple(
            [
                # belongs to state1
                {"attr1": True, "idem": 1},
                {"attr1": True, "idem": 2},
                {"attr1": True, "idem": 3},
                # belongs to state2
                {"attr2": True, "idem": 4},
                # belongs to state3
                {"attr3": True, "idem": 5},
            ],
            "idem",
        )
        pipeline.assert_valid_state_migrations(self.content_store, 2)

    def test_assert_missing_doc_invalid(self):
        pipeline = Pipeline("demo")
        pipeline.add_state(PipelineState("state1", {"attr1": True}), is_starting=True)
        pipeline.add_state(PipelineState("state2", {"attr2": True}))
        pipeline.add_state(PipelineState("state3", {"attr3": True}))
        self.content_store.append_multiple(
            [
                # belongs to state1
                {"attr1": True, "idem": 1},
                {"attr1": True, "idem": 2},
                {"attr1": True, "idem": 3},
                # belongs to state2
                {"attr2": True, "idem": 4},
                # belongs no state
                {"attr4": True, "idem": 5},
            ],
            "idem",
        )
        self.assertRaisesRegex(
            RuntimeError,
            "Sum of all state docs does not match total count",
            pipeline.assert_valid_state_migrations,
            self.content_store,
            2,
        )

    def test_assert_duplicate_doc_invalid(self):
        pipeline = Pipeline("demo")
        pipeline.add_state(PipelineState("state1", {"attr1": True}), is_starting=True)
        pipeline.add_state(PipelineState("state2", {"attr2": True}))
        pipeline.add_state(PipelineState("state3", {"attr3": True}))
        self.content_store.append_multiple(
            [
                # belongs to state1
                {"attr1": True, "idem": 1},
                {"attr1": True, "idem": 2},
                {"attr1": True, "idem": 3},
                # belongs to state2
                {"attr2": True, "idem": 4},
                # belongs to state2 and state3
                {"attr2": True, "attr3": True, "idem": 5},
            ],
            "idem",
        )
        self.assertRaisesRegex(
            RuntimeError,
            "is going to have both",
            pipeline.assert_valid_state_migrations,
            self.content_store,
            2,
        )

    def test_assert_tricky_missing_and_duplicate_doc_invalid(self):
        pipeline = Pipeline("demo")
        pipeline.add_state(PipelineState("state1", {"attr1": True}), is_starting=True)
        pipeline.add_state(PipelineState("state2", {"attr2": True}))
        pipeline.add_state(PipelineState("state3", {"attr3": True}))
        self.content_store.append_multiple(
            [
                # belongs to state1
                {"attr1": True, "idem": 1},
                {"attr1": True, "idem": 2},
                {"attr1": True, "idem": 3},
                # belongs to no state
                {"attr4": True, "idem": 4},
                # belongs to state2 and state3
                {"attr2": True, "attr3": True, "idem": 5},
            ],
            "idem",
        )
        self.assertRaisesRegex(
            RuntimeError,
            "is going to have both",
            pipeline.assert_valid_state_migrations,
            self.content_store,
            2,
        )


class TestPipelineMigrate(TestPipeline):
    def test_successful_migration(self):
        pipeline = Pipeline("demo")
        pipeline.add_state(PipelineState("state1", {"attr1": True}), is_starting=True)
        pipeline.add_state(PipelineState("state2", {"attr2": True}))
        pipeline.add_state(PipelineState("state3", {"attr3": True}))
        self.content_store.append_multiple(
            [
                # belongs to state1
                {"attr1": True, "idem": 1},
                {"attr1": True, "idem": 2},
                {"attr1": True, "idem": 3},
                # belongs to state2
                {"attr2": True, "idem": 4},
                # belongs to state3
                {"attr3": True, "idem": 5},
            ],
            "idem",
        )
        pipeline.perform_state_migrations(self.content_store)
        assert self.actual_documents_without_id() == [
            {"attr1": True, "idem": 1, "_state": "state1"},
            {"attr1": True, "idem": 2, "_state": "state1"},
            {"attr1": True, "idem": 3, "_state": "state1"},
            {"attr2": True, "idem": 4, "_state": "state2"},
            {"attr3": True, "idem": 5, "_state": "state3"},
        ]

    def test_successful_idempotent_migration(self):
        pipeline = Pipeline("demo")
        pipeline.add_state(PipelineState("state1", {"attr1": True}), is_starting=True)
        pipeline.add_state(PipelineState("state2", {"attr2": True}))
        pipeline.add_state(PipelineState("state3", {"attr3": True}))
        self.content_store.append_multiple(
            [
                # belongs to state1
                {"attr1": True, "idem": 1},
                {"attr1": True, "idem": 2},
                {"attr1": True, "idem": 3},
                # belongs to state2
                {"attr2": True, "idem": 4},
                # belongs to state3
                {"attr3": True, "idem": 5},
            ],
            "idem",
        )
        pipeline.perform_state_migrations(self.content_store)

        # simulate a failed migration here
        self.content_store.update_many(
            filter_q={"attr1": True}, update_doc={"$unset": {"_state": ""}}
        )

        pipeline.perform_state_migrations(self.content_store)
        assert self.actual_documents_without_id() == [
            {"attr1": True, "idem": 1, "_state": "state1"},
            {"attr1": True, "idem": 2, "_state": "state1"},
            {"attr1": True, "idem": 3, "_state": "state1"},
            {"attr2": True, "idem": 4, "_state": "state2"},
            {"attr3": True, "idem": 5, "_state": "state3"},
        ]
