from typing import Dict, List
import unittest

import mongomock
import pymongo

from broccoli_server.content import ContentStore
from broccoli_server.worker.metadata_store import MetadataStoreFactory


# can't skip this
class TestCaseWithMongoMock(unittest.TestCase):
    @classmethod
    @mongomock.patch("mongodb://localhost:27017/test_db")
    def setUpClass(cls) -> None:
        cls.content_store = ContentStore("localhost:27017", "test_db")
        cls.metadata_store_factory = MetadataStoreFactory("localhost:27017", "test_db")

    def tearDown(self) -> None:
        self.content_store.client.drop_database("test_db")

    def actual_documents_by_id_desc(self) -> List[Dict]:
        actual_documents = []
        for d in self.content_store.collection.find(
            {}, sort=[("_id", pymongo.DESCENDING)]
        ):
            actual_documents.append(d)
        return actual_documents

    def actual_documents_without_id(self) -> List[Dict]:
        actual_cursor = self.content_store.collection.find({})
        actual_documents = []
        for actual_document in actual_cursor:
            del actual_document["_id"]
            actual_documents.append(actual_document)
        return actual_documents
