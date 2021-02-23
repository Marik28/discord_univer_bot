import unittest

from config import TEST_DB
from redis_utils.redis_api import RedisSetManager, get_redis_connection

connection = get_redis_connection(db=TEST_DB)
set_name = "test_set"


class RedisSetTests(unittest.TestCase):
    """Тестируем наш класс для управления сетом в Redis"""

    def setUp(self) -> None:
        self.connection = connection
        self.set = RedisSetManager(connection, set_name)

    def tearDown(self) -> None:
        self.set.clear()
        self.connection.close()

    def test_add_method(self):
        assert self.connection.scard(set_name) == 0
        value = "example"
        self.set.add(value)
        assert self.connection.scard(set_name) == 1, "При добавлении элемента во множесто, его размер увеличивается"
        self.connection.delete(set_name)

    def test_len_function(self):
        assert len(self.set) == 0
        self.connection.sadd(set_name, "value")
        assert len(self.set) == 1
        self.connection.delete(set_name)


if __name__ == '__main__':
    unittest.main()