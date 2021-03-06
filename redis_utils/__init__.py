from config import ANIME_LINKS_DB, ANIME_LINKS_SET
from redis_utils.redis_handlers import get_redis_connection
from redis_utils.redis_hash import RedisHashManager, CounterHashManager
from redis_utils.redis_set import LinksSetManager, RedisSetManager


test_set_name = "test_set"
test_hash_name = "test_hash"
test_counter_name = "test_counter"

redis_conn = get_redis_connection(db=ANIME_LINKS_DB)
links_set_manager = LinksSetManager(redis_conn, ANIME_LINKS_SET)
rolls_counter = CounterHashManager(redis_conn, "rolls")

test_set = RedisSetManager(redis_conn, test_set_name)
test_hash = RedisHashManager(redis_conn, test_hash_name)
test_counter = CounterHashManager(redis_conn, test_counter_name)
