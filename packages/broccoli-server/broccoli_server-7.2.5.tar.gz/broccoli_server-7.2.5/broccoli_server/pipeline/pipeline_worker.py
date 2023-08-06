import dataclasses
from typing import Callable, Dict, List, Optional, Set

from broccoli_server.interface.worker import WorkContext

from .state_update import StateUpdate


@dataclasses.dataclass
class PipelineWorker:
    name: str
    process: Callable[[WorkContext, List[Dict]], List[StateUpdate]]
    from_state: str
    to_states: Set[str]
    limit: Optional[int] = None
    sort: Optional[Dict] = None

    def to_dict(self):
        return {
            "name": self.name,
            "from_state": self.from_state,
            "to_states": list(sorted(self.to_states)),
        }
