import abc
import copy
from typing import Dict, List, Optional, Set

from pymongo import UpdateMany

from broccoli_server.interface.worker import WorkContext
from broccoli_server.interface.worker import Worker

from .state_key import StateKey
from .state_update import StateUpdate


class PipelineWorkerClass(Worker, abc.ABC):
    """
    PipelineWorker's API is represented as an object rather than the traditional Broccoli Worker class inheritance
    So this class is essentially the bridge
    """

    def __init__(
        self,
        pipeline_name: str,
        from_state: str,
        to_states: Set[str],
        limit: Optional[int],
        sort: Optional[Dict],
    ):
        self.pipeline_name = pipeline_name
        self.from_state = from_state
        self.to_states = to_states
        self.limit = limit
        self.sort = sort

    @abc.abstractmethod
    def pre_work(self, context: WorkContext):
        pass

    def work(self, context: WorkContext):
        from_state_documents = context.content_store().query(
            q={StateKey: self.from_state}, limit=self.limit, sort=self.sort
        )
        if not from_state_documents:
            context.logger().info(f"No item in {self.from_state} state")
            return

        context.logger().info(
            f"{len(from_state_documents)} items in {self.from_state} state"
        )
        all_results = self.process(context, from_state_documents)

        valid_results = []
        for state_update in all_results:
            if state_update.to_state not in self.to_states:
                context.logger().error(
                    f"{state_update.to_state} is not a designated terminal state"
                )
            else:
                valid_results.append(state_update)

        if not valid_results:
            context.logger().info("No item to transit state for")
            return

        context.logger().info(f"Transitioning state for {len(valid_results)} item(s)")

        def transform_state_update(_state_update: StateUpdate):
            update_doc = _state_update.update_doc if _state_update.update_doc else {}
            new_update_doc = copy.deepcopy(update_doc)
            # manually $set the StateKey update so that it does the least amount of disrupt to the original update_doc
            # e.g. otherwise other fields in $set in update_doc might be override
            if "$set" not in new_update_doc:
                new_update_doc["$set"] = {}
            new_update_doc["$set"][StateKey] = _state_update.to_state
            return UpdateMany(filter=_state_update.filter_q, update=new_update_doc)

        context.content_store().collection.bulk_write(
            requests=list(map(transform_state_update, valid_results)), ordered=False
        )

    @abc.abstractmethod
    def process(self, context: WorkContext, documents: List[Dict]) -> List[StateUpdate]:
        pass
