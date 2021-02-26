from redis import Redis


class RedisCounter:
    def __init__(self, redis_: Redis):
        self._redis = redis_

    def increment(self, key: str) -> int:
        return self._redis.incr(key)

    def get_counts(self, key: str) -> int:
        value: str = self._redis.get(key)
        try:
            return int(value)
        except ValueError:
            return 0
