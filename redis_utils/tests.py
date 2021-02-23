import unittest

from redis_utils.redis_api import RedisSetManager, redis_conn


class RedisSetTests(unittest.TestCase):
    """Тестируем наш класс для управления сетом в Redis"""
    connection = redis_conn
    set_name = "test_set"

    def setUp(self) -> None:
        self.set = RedisSetManager(redis_conn, self.set_name)

    def tearDown(self) -> None:
        self.set.clear()
        self.connection.close()

    def test_adding_element_and_len_func(self):
        elem_1 = "1"
        elem_2 = "2"
        assert len(self.set) == 0, "Изначально множество пустое"
        self.set.add(elem_1)
        assert len(self.set) == 1, "Добавили элемент, теперь длина == 1"
        self.set.add(elem_2)
        assert len(self.set) == 2
        self.set.clear()

    def test_adding_and_popping_an_element(self):
        elem = "1"
        assert len(self.set) == 0
        self.set.add(elem)
        assert len(self.set) == 1
        assert self.set.pop() == elem, "Возвращает тот же элемент что и был добавлен"
        assert len(self.set) == 0


if __name__ == '__main__':
    unittest.main()