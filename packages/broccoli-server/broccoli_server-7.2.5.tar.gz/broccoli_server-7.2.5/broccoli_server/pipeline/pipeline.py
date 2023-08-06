import copy
from typing import Dict, List, Optional, Set

from broccoli_server.content import ContentStore

from .pipeline_mod_view import PipelineModView
from .pipeline_state import PipelineState
from .pipeline_worker import PipelineWorker
from .state_key import StateKey


class Pipeline(object):
    def __init__(self, name: str):
        self.name = name
        self.states = []  # type: List[PipelineState]
        self.starting_state = None  # type: Optional[PipelineState]
        self.workers = []  # type: List[PipelineWorker]
        self.mod_views = []  # type: List[PipelineModView]
        self._graph_adj_list = {}  # type: Dict[str, List[str]]

    def add_state(self, state: PipelineState, is_starting: bool = False):
        if state in self._get_state_names():
            raise RuntimeError(
                f"For pipeline {self.name} state {state.name} already exists"
            )
        if is_starting:
            if self.starting_state:
                raise RuntimeError(
                    f"For pipeline {self.name} starting state is already set"
                )
            self.starting_state = state
        self.states.append(state)

    def _get_state_names(self) -> List[str]:
        return list(map(lambda s: s.name, self.states))

    def add_worker(self, worker: PipelineWorker):
        from_state = worker.from_state
        to_states = worker.to_states
        if from_state not in self._get_state_names():
            raise RuntimeError(
                f"For pipeline {self.name} {from_state} is not (yet) a valid state"
            )
        for to_state in to_states:
            if to_state not in self._get_state_names():
                raise RuntimeError(
                    f"For pipeline {self.name} {to_state} is not (yet) a valid state"
                )
        self.workers.append(worker)
        if from_state not in self._graph_adj_list:
            self._graph_adj_list[from_state] = []
        self._graph_adj_list[from_state] += list(to_states)

    def add_mod_view(self, mod_view: PipelineModView):
        from_state = mod_view.from_state
        to_states = mod_view.to_state_names()
        if from_state not in self._get_state_names():
            raise RuntimeError(
                f"For pipeline {self.name} {from_state} is not (yet) a valid state"
            )
        for to_state in to_states:
            if to_state not in self._get_state_names():
                raise RuntimeError(
                    f"For pipeline {self.name} {to_state} is not (yet) a valid state"
                )
        self.mod_views.append(mod_view)
        if from_state not in self._graph_adj_list:
            self._graph_adj_list[from_state] = []
        self._graph_adj_list[from_state] += list(to_states)

    def assert_pipeline_is_dag(self):
        discovered = set()  # type: Set[str]
        visiting = set()  # type: Set[str]

        def has_cycle(state_name: str) -> bool:
            discovered.add(state_name)
            visiting.add(state_name)
            for to_state in self._graph_adj_list.get(state_name, []):
                if to_state not in discovered:
                    if has_cycle(to_state):
                        return True
                elif to_state in visiting:
                    return True
            visiting.remove(state_name)
            return False

        if not self.starting_state:
            raise RuntimeError(f"Pipeline {self.name} does not have a starting state")
        if has_cycle(self.starting_state.name):
            raise RuntimeError(f"Pipeline {self.name} has a cycle")

        undiscovered = set(self._get_state_names()) - discovered
        if undiscovered:
            raise RuntimeError(f"States {', '.join(undiscovered)} are undiscovered")

    @staticmethod
    def _if_all_items_have_state(content_store: ContentStore) -> bool:
        return content_store.count({StateKey: {"$exists": False}}) == 0

    def _object_ids_missing_migration(self, content_store: ContentStore) -> List[str]:
        all_docs_ids = set()
        for doc in content_store.collection.find({}, {"_id": 1}):
            all_docs_ids.add(str(doc["_id"]))

        migrated_doc_ids = set()
        for state in self.states:
            for doc in content_store.collection.find(state.migrate_q, {"_id": 1}):
                migrated_doc_ids.add(str(doc["_id"]))

        return list(sorted(all_docs_ids - migrated_doc_ids))

    def assert_valid_state_migrations(
        self, content_store: ContentStore, migration_batch: int = 50
    ):
        if self._if_all_items_have_state(content_store):
            print(f"Pipeline {self.name} has migrated state for all items")
            return

        # quickly check count first
        # if sum of all state docs < total count then there are docs that are unmigrated and it has to be invalid
        sum_migrated_count = 0
        for state in self.states:
            sum_migrated_count += content_store.count(state.migrate_q)
        total_count = content_store.count({})
        if sum_migrated_count < total_count:
            print(
                f"Sampling 100 object IDs that will miss migration {self._object_ids_missing_migration(content_store)[: 100]}"
            )
            raise RuntimeError(
                f"Sum of all state docs does not match total count. sum={sum_migrated_count} < actual={total_count}"
            )

        # check if there is overlap in state docs
        # combined with the check that count matches, it means
        # every item in content store belongs to one and only one state
        # and all items in content store are accounted for
        doc_id_to_state = {}  # type: Dict[str, PipelineState]
        for state in self.states:
            state_name = state.name
            migrate_q = state.migrate_q
            migrated_count = content_store.count(state.migrate_q)
            migration_batches = migrated_count // migration_batch

            for i in range(migration_batches):
                print(
                    f"Checking pipeline {self.name} state {state_name} migration batch {i + 1}/{migration_batches}"
                )
                for doc in content_store.query(
                    migrate_q, skip=i * migration_batch, limit=migration_batch
                ):
                    doc_id = doc["_id"]
                    if doc_id in doc_id_to_state:
                        raise RuntimeError(
                            f"Document with id {doc_id} is going to have "
                            f"both {doc_id_to_state[doc_id].name} and {state.name} state"
                        )
                    doc_id_to_state[doc_id] = state

            print(
                f"Checking pipeline {self.name} state {state_name} last migration batch"
            )
            for doc in content_store.query(
                migrate_q, skip=migration_batches * migration_batch
            ):
                doc_id = doc["_id"]
                if doc_id in doc_id_to_state:
                    raise RuntimeError(
                        f"Document with id {doc_id} is going to have "
                        f"both {doc_id_to_state[doc_id].name} and {state.name} state"
                    )
                doc_id_to_state[doc_id] = state

    def perform_state_migrations(self, content_store: ContentStore):
        if self._if_all_items_have_state(content_store):
            print(f"Pipeline {self.name} has migrated state for all items")
            return

        for state in self.states:
            print(f"Migrating pipeline {self.name} state {state.name}")
            # putting StateKey: ... after so that it has the final say on StateKey
            filter_q = state.migrate_q if state.migrate_q else {}
            new_filter_q = copy.deepcopy(filter_q)
            new_filter_q[StateKey] = {"$exists": False}
            if content_store.count(new_filter_q) != 0:
                content_store.update_many(
                    filter_q=new_filter_q, update_doc={"$set": {StateKey: state.name}}
                )
            else:
                print(
                    f"No document to migrate for pipeline {self.name} state {state.name}"
                )

    def to_dict(self, content_store: ContentStore):
        if not self.starting_state:
            raise RuntimeError(f"Pipeline {self.name} does not have a starting state")
        return {
            "states": list(map(lambda s: s.to_dict(content_store), self.states)),
            "starting_state": self.starting_state.to_dict(content_store),
            "workers": list(map(PipelineWorker.to_dict, self.workers)),
            "mod_views": list(map(PipelineModView.to_dict, self.mod_views)),
        }
