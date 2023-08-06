import bson
import pymongo

from .testcase_with_mongomock import TestCaseWithMongoMock


class TestContentStoreAppend(TestCaseWithMongoMock):
    def test_idempotency_key_absent(self):
        self.content_store.append({}, "idempotency_key")
        assert self.content_store.collection.count_documents({}) == 0

    def test_idempotency_value_exists(self):
        self.content_store.append({"idempotency_key": "some_value"}, "idempotency_key")
        self.content_store.append({"idempotency_key": "some_value"}, "idempotency_key")
        assert (
            self.content_store.collection.count_documents(
                {"idempotency_key": "some_value"}
            )
            == 1
        )

    def test_succeed(self):
        self.content_store.append({"key": "value_1"}, "key")
        self.content_store.append({"key": "value_2"}, "key")
        assert self.actual_documents_without_id() == [
            {
                "key": "value_1",
            },
            {
                "key": "value_2",
            },
        ]


class TestContentStoreAppendMultiple(TestCaseWithMongoMock):
    def test_idempotency_key_absent(self):
        self.content_store.append_multiple(
            [{"key": "value1"}, {"key2": "value2"}], "key2"
        )
        assert self.actual_documents_without_id() == [
            {
                "key2": "value2",
            }
        ]

    def test_idempotency_value_exists_in_persistence(self):
        self.content_store.append({"key": "value"}, "key")
        self.content_store.append_multiple([{"key": "value"}, {"key": "value2"}], "key")
        assert self.actual_documents_without_id() == [
            {
                "key": "value",
            },
            {
                "key": "value2",
            },
        ]

    def test_idempotency_value_exists_in_persistence_and_nothing_to_append(self):
        self.content_store.append({"key": "value"}, "key")
        self.content_store.append_multiple(
            [
                {"key": "value"},
            ],
            "key",
        )
        assert self.actual_documents_without_id() == [
            {
                "key": "value",
            }
        ]

    def test_idempotency_value_exists_in_batch(self):
        self.content_store.append_multiple(
            [{"key": "value", "foo": "bar"}, {"key": "value"}, {"key": "value2"}], "key"
        )
        assert self.actual_documents_without_id() == [
            {
                "key": "value",
                "foo": "bar",
            },
            {
                "key": "value2",
            },
        ]

    def test_succeed(self):
        self.content_store.append({"key": "value"}, "key")
        self.content_store.append_multiple(
            [{"key": "value2"}, {"key": "value3"}], "key"
        )
        assert self.actual_documents_without_id() == [
            {
                "key": "value",
            },
            {
                "key": "value2",
            },
            {
                "key": "value3",
            },
        ]


class TestContentStoreQueryAndCount(TestCaseWithMongoMock):
    def test_succeed_lt_gt_id(self):
        self.content_store.append({"key": "value_1", "attr1": False}, "key")
        self.content_store.append({"key": "value_2", "attr1": False}, "key")
        self.content_store.append({"key": "value_3", "attr1": True}, "key")
        self.content_store.append({"key": "value_4", "attr1": False}, "key")
        self.content_store.append({"key": "value_5", "attr1": True}, "key")
        self.content_store.append({"key": "value_6", "attr1": True}, "key")
        lt = self.content_store.query(q={"key": "value_6"})
        assert (
            self.content_store.query(
                q={"attr1": True, "_id": {"$lt": bson.ObjectId(lt[0]["_id"])}},
                limit=1,
                projection=["key"],
                sort={"_id": pymongo.DESCENDING},
                skip=1,
            )[0]["key"]
            == "value_3"
        )
        lt2 = self.content_store.query(q={"key": "value_3"})
        assert not self.content_store.query(
            q={"attr1": True, "_id": {"$lt": bson.ObjectId(lt2[0]["_id"])}},
            limit=1,
            projection=["key"],
            sort={"_id": pymongo.DESCENDING},
            skip=1,
        )
        gt = self.content_store.query(q={"key": "value_3"})
        assert (
            self.content_store.count(
                q={"attr1": True, "_id": {"$gt": bson.ObjectId(gt[0]["_id"])}},
                sort={"_id": pymongo.DESCENDING},
            )
            == 2
        )

    def test_succeed_multiple_sort(self):
        self.content_store.append({"key": "value_1", "ts": 1}, "key")
        self.content_store.append({"key": "value_2", "ts": 1}, "key")
        self.content_store.append({"key": "value_3", "ts": 2}, "key")
        self.content_store.append({"key": "value_4", "ts": 3}, "key")
        self.content_store.append({"key": "value_5", "ts": 4}, "key")
        self.content_store.append({"key": "value_6", "ts": 4}, "key")
        docs = self.content_store.query(
            q={},
            sort={"ts": pymongo.DESCENDING, "_id": pymongo.ASCENDING},
        )
        assert list(map(lambda d: d["key"], docs)) == [
            "value_5",
            "value_6",
            "value_4",
            "value_3",
            "value_1",
            "value_2",
        ]


class TestContentStoreQueryNearestNeighbors(TestCaseWithMongoMock):
    def test_invalid_from_binary_string(self):
        assert (
            self.content_store.query_nearest_hamming_neighbors(
                q={},
                binary_string_key="binary_string_key",
                from_binary_string="abc",
                max_distance=5,
            )
            == []
        )

    def test_query_do_not_match(self):
        self.content_store.append({"key": "value_1", "bs": "0000"}, "key")
        self.content_store.append({"key": "value_2", "bs": "0000"}, "key")
        assert (
            self.content_store.query_nearest_hamming_neighbors(
                q={"key": "value_3"},
                binary_string_key="bs",
                from_binary_string="0000",
                max_distance=1,
            )
            == []
        )

    def test_query_results_do_not_have_field(self):
        self.content_store.append({"key": "value_1", "bs_key_2": "0000"}, "key")
        self.content_store.append({"key": "value_2", "bs_key_2": "0000"}, "key")
        assert (
            self.content_store.query_nearest_hamming_neighbors(
                q={}, binary_string_key="bs", from_binary_string="0000", max_distance=1
            )
            == []
        )

    def test_query_results_do_not_have_same_length_string(self):
        self.content_store.append({"key": "value_1", "bs": "0000"}, "key")
        self.content_store.append({"key": "value_2", "bs": "0000"}, "key")
        assert (
            self.content_store.query_nearest_hamming_neighbors(
                q={}, binary_string_key="bs", from_binary_string="00001", max_distance=1
            )
            == []
        )

    def test_query_results_do_not_have_valid_binary_string(self):
        self.content_store.append({"key": "value_1", "bs": "abcd"}, "key")
        self.content_store.append({"key": "value_2", "bs": "abcd"}, "key")
        assert (
            self.content_store.query_nearest_hamming_neighbors(
                q={}, binary_string_key="bs", from_binary_string="0000", max_distance=1
            )
            == []
        )

    def test_succeed(self):
        self.content_store.append({"key": "value_1", "attr": True, "bs": "0000"}, "key")
        self.content_store.append({"key": "value_2", "attr": True, "bs": "0001"}, "key")
        self.content_store.append({"key": "value_3", "attr": True, "bs": "1111"}, "key")
        self.content_store.append(
            {"key": "value_4", "attr": False, "bs": "0000"}, "key"
        )
        actual_documents = self.content_store.query_nearest_hamming_neighbors(
            q={"attr": True},
            binary_string_key="bs",
            from_binary_string="0000",
            max_distance=1,
        )
        for i in range(len(actual_documents)):
            del actual_documents[i]["_id"]
        assert actual_documents == [
            {
                "key": "value_1",
                "attr": True,
                "bs": "0000",
            },
            {
                "key": "value_2",
                "attr": True,
                "bs": "0001",
            },
        ]


class TestContentStoreQueryNNearestNeighbors(TestCaseWithMongoMock):
    def test_invalid_from_binary_string(self):
        assert (
            self.content_store.query_n_nearest_hamming_neighbors(
                q={},
                binary_string_key="binary_string_key",
                from_binary_string="abc",
                pick_n=0,
            )
            == []
        )

    def test_query_do_not_match(self):
        self.content_store.append({"key": "value_1", "bs": "0000"}, "key")
        self.content_store.append({"key": "value_2", "bs": "0001"}, "key")
        assert (
            self.content_store.query_n_nearest_hamming_neighbors(
                q={"key": "value_3"},
                binary_string_key="bs",
                from_binary_string="0000",
                pick_n=1,
            )
            == []
        )

    def test_query_results_do_not_have_field(self):
        self.content_store.append({"key": "value_1", "bs_key_2": "0000"}, "key")
        self.content_store.append({"key": "value_2", "bs_key_2": "0001"}, "key")
        assert (
            self.content_store.query_n_nearest_hamming_neighbors(
                q={}, binary_string_key="bs", from_binary_string="0000", pick_n=1
            )
            == []
        )

    def test_query_results_do_not_have_same_length_string(self):
        self.content_store.append({"key": "value_1", "bs": "0000"}, "key")
        self.content_store.append({"key": "value_2", "bs": "0001"}, "key")
        assert (
            self.content_store.query_n_nearest_hamming_neighbors(
                q={}, binary_string_key="bs", from_binary_string="00001", pick_n=1
            )
            == []
        )

    def test_query_results_do_not_have_valid_binary_string(self):
        self.content_store.append({"key": "value_1", "bs": "abcd"}, "key")
        self.content_store.append({"key": "value_2", "bs": "abcd"}, "key")
        assert (
            self.content_store.query_n_nearest_hamming_neighbors(
                q={}, binary_string_key="bs", from_binary_string="0000", pick_n=1
            )
            == []
        )

    def test_succeed(self):
        self.content_store.append({"key": "value_1", "attr": True, "bs": "0001"}, "key")
        self.content_store.append({"key": "value_2", "attr": True, "bs": "0011"}, "key")
        self.content_store.append({"key": "value_3", "attr": True, "bs": "0011"}, "key")
        self.content_store.append({"key": "value_4", "attr": True, "bs": "0111"}, "key")
        self.content_store.append(
            {"key": "value_5", "attr": False, "bs": "0000"}, "key"
        )
        actual_documents = self.content_store.query_n_nearest_hamming_neighbors(
            q={"attr": True},
            binary_string_key="bs",
            from_binary_string="0000",
            pick_n=2,
        )
        for i in range(len(actual_documents)):
            del actual_documents[i]["_id"]
        assert actual_documents == [
            {
                "key": "value_3",
                "attr": True,
                "bs": "0011",
            },
            {
                "key": "value_1",
                "attr": True,
                "bs": "0001",
            },
        ]
