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
        self.connection.delete(set_name)
        self.connection.close()

    def test_add_method(self):
        assert self.connection.scard(set_name) == 0
        value = "example"
        self.set.add(value)
        assert self.connection.scard(set_name) == 1, "При добавлении элемента во множесто, его размер увеличивается"
        assert self.connection.srandmember(set_name).decode() == value, \
            "Единственный рандомный элемент будет тот же, что мы добавили"
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


if __name__ == '__main__':
    unittest.main()
