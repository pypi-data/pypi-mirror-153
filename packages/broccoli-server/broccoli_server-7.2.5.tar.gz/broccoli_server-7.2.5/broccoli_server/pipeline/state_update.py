import dataclasses
from typing import Dict, Optional


@dataclasses.dataclass
class StateUpdate:
    filter_q: Dict
    to_state: str
    update_doc: Optional[Dict] = None
