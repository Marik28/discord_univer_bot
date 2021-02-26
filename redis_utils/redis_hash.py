from collections import KeysView, ValuesView
from typing import Union, Iterator, ItemsView

from redis import Redis


class RedisHashManager:
    """Класс-обертка над Hash Redis"""
    def __init__(self, redis_: Redis, hash_name: str):
        self._redis = redis_
        self._hash_name = hash_name

    def get(self, item: str, default: str = None) -> Union[str, None]:
        result: str = self._redis.hget(self._hash_name, item)
        if result is None:
            return default
        else:
            return result

    def values(self) -> ValuesView[str]:
        values: list[str] = self._redis.hvals(self._hash_name)
        return ValuesView(values)

    def keys(self) -> KeysView[str]:
        keys: list[str] = self._redis.hkeys(self._hash_name)
        return KeysView(set(keys))

    def items(self) -> ItemsView[str, str]:
        items: dict[str, str] = self._redis.hgetall(self._hash_name)
        return ItemsView(items)

    def clear(self) -> None:
        self._redis.delete(self._hash_name)

    def discard(self, item: str) -> None:
        self._redis.hdel(self._hash_name, item)

    def __contains__(self, item: str) -> bool:
        return self._redis.hexists(self._hash_name, item)

    def __setitem__(self, key: str, value: str) -> None:
        self._redis.hset(self._hash_name, key, value)

    def __len__(self) -> int:
        return self._redis.hlen(self._hash_name)

    def __getitem__(self, item: str) -> str:
        result: str = self._redis.hget(self._hash_name, item)
        if result is None:
            raise KeyError(f"Данного ключа нет в `словаре` {self._hash_name}")
        else:
            return result
