import dataclasses
from typing import Dict

from broccoli_server.content import ContentStore

from .state_key import StateKey


@dataclasses.dataclass
class PipelineState:
    name: str
    migrate_q: Dict

    def to_dict(self, content_store: ContentStore):
        return {
            "name": self.name,
            "count": content_store.collection.count_documents({StateKey: self.name}),
        }
