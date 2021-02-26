import unittest

from config import TEST_DB
from redis_utils import get_redis_connection, RedisSetManager

connection = get_redis_connection(db=TEST_DB)
set_name = "test_set"


class RedisSetTests(unittest.TestCase):
    """Тестируем наш класс для управления сетом в Redis"""

    def setUp(self) -> None:
        self.connection = connection
        self.connection.delete(set_name)
        self.set = RedisSetManager(connection, set_name)

    def tearDown(self) -> None:
        self.connection.delete(set_name)
        self.connection.close()

    def test_add_method(self):
        assert self.connection.scard(set_name) == 0
        value = "example"
        self.set.add(value)
        assert self.connection.scard(set_name) == 1, "При добавлении элемента во множесто, его размер увеличивается"
        assert self.connection.sismember(set_name, value) is True, \
            "элемент присутствует во множестве"
        self.connection.delete(set_name)

    def test_len_method(self):
        assert len(self.set) == 0
        self.connection.sadd(set_name, "value")
        assert len(self.set) == 1
        self.connection.delete(set_name)
        assert len(self.set) == 0

    def test_len_method_with_more_data(self):
        elements = [str(num) for num in range(10)]
        self.connection.sadd(set_name, *elements)
        assert len(self.set) == len(elements)

    def test_clear_method(self):
        self.connection.sadd(set_name, "element")
        self.set.clear()
        assert self.connection.scard(set_name) == 0

    def test_contains_method_with_existing_item(self):
        item = "test_item"
        self.connection.sadd(set_name, item)
        self.assertTrue(item in self.set)

    def test_contains_method_with_non_existing_item(self):
        self.connection.delete(set_name)
        item = "test"
        self.assertFalse(item in self.set)

    def test_update_method(self):
        items = ["1", "2", "3"]
        self.set.update(items)
        for item in items:
            self.assertTrue(self.connection.sismember(set_name, item))

    def test_iter_method(self):
        items = {"1", "2", "3"}
        self.connection.sadd(set_name, *items)
        from_redis = {elem for elem in self.set}
        assert items == from_redis

    def test_iter_with_empty_set(self):
        assert len({elem for elem in self.set}) == 0


if __name__ == '__main__':
    unittest.main()
