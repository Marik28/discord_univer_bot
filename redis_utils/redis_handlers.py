from redis import Redis

from config import REDIS_HOST, REDIS_PORT


def get_redis_connection(host=REDIS_HOST, port=REDIS_PORT, db=0) -> Redis:
    return Redis(host=host, port=port, db=db, decode_responses=True)
