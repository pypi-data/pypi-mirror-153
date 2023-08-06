import json
from typing import Dict

from broccoli_server.content import ContentStore
from broccoli_server.interface.mod_view import NonCallbackModViewColumn
from broccoli_server.interface.mod_view.column_render import Text


class Echo(NonCallbackModViewColumn):
    def __init__(self, key: str):
        self.key = key

    def render(self, document: Dict, content_store: ContentStore) -> Text:
        if self.key in document:
            return Text(text=json.dumps(document[self.key], ensure_ascii=False))
        else:
            return Text(text="N/A")
