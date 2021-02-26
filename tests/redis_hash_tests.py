import random
import unittest

from config import TEST_DB
from redis_utils import redis_conn, test_hash_name, get_redis_connection, RedisHashManager

connection = get_redis_connection(db=TEST_DB)


class TestRedisHash(unittest.TestCase):

    hash_ = RedisHashManager(redis_conn, test_hash_name)
    redis_ = redis_conn

    def tearDown(self) -> None:
        self.redis_.delete(test_hash_name)

    def test_get_item_method(self):
        d = {str(random.randint(1, 1000)): str(random.randint(1, 1000)) for i in range(100)}
        self.redis_.hset(test_hash_name, mapping=d)
        for key, value in d.items():
            assert self.hash_[key] == value

    def test_len(self):
        d = {str(random.randint(1, 1000)): str(random.randint(1, 1000)) for i in range(100)}
        self.redis_.hset(test_hash_name, mapping=d)
        assert len(d) == len(self.hash_)

    def test_contains(self):
        d = {str(random.randint(1, 1000)): str(random.randint(1, 1000)) for i in range(100)}
        self.redis_.hset(test_hash_name, mapping=d)
        for key in d:
            assert key in self.hash_

    # def test_set_item(self):
    #     d = {str(random.randint(1, 1000)): str(random.randint(1, 1000)) for i in range(100)}
    #     for key, value in d:
    #         self.hash_[key] = value
    #     assert