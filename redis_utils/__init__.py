from config import ANIME_LINKS_DB, ANIME_LINKS_SET
from redis_utils.redis_handlers import get_redis_connection
from redis_utils.redis_hash import RedisHashManager
from redis_utils.redis_set import LinksSetManager, RedisSetManager

redis_conn = get_redis_connection(db=ANIME_LINKS_DB)
links_set_manager = LinksSetManager(redis_conn, ANIME_LINKS_SET)
test_set = RedisSetManager(redis_conn, "test_set")
test_hash = RedisHashManager(redis_conn, "test_hash")
