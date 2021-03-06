from collections import KeysView, ValuesView
from typing import Union, Iterator, ItemsView, Mapping

from redis import Redis


class RedisHashManager:
    """Класс-обертка над Hash Redis. Имеет API как встроенный `dict`"""

    def __init__(self, redis_: Redis, hash_name: str) -> None:
        """Для инициализации принимает `Redis` и имя Hash `hash_name`, с которым будет работать.
        Redis обязательно должен быть инициализирован с `decode_responses=True`"""
        self._redis = redis_
        self._hash_name = hash_name

    def get(self, item: str, default: str = None) -> Union[str, None]:
        """Возвращает значение по ключу `item`, если он есть в hash, иначе возвращает `default`"""
        result: str = self._redis.hget(self._hash_name, item)
        if result is None:
            return default
        else:
            return result

    def values(self) -> ValuesView[str]:
        """Возвращает множество всех значений в виде ValuesView"""
        values: list[str] = self._redis.hvals(self._hash_name)
        return ValuesView(values)

    def keys(self) -> KeysView[str]:
        """Возвращает множество всех ключей в виде KeysView"""
        keys: list[str] = self._redis.hkeys(self._hash_name)
        return KeysView(keys)

    def items(self) -> ItemsView[str, str]:
        """Возвращает множество пар ключ-значение в виде ItemsView"""
        items: dict[str, str] = self._redis.hgetall(self._hash_name)
        return ItemsView(items)

    def clear(self) -> None:
        """Полностью очищает Hash"""
        self._redis.delete(self._hash_name)

    def discard(self, item: str) -> None:
        """Удаляет переданный элемент `item` из Hash"""
        self._redis.hdel(self._hash_name, item)

    def update(self, mapping: Mapping[str, str]) -> None:
        """Добавляет или обновляет ключи со значениями из `mapping`"""
        self._redis.hset(self._hash_name, mapping=mapping)

    def __contains__(self, item: str) -> bool:
        """Возвращает True, если элемент `item` является ключом данного Hash, иначе False"""
        return self._redis.hexists(self._hash_name, item)

    def __setitem__(self, key: str, value: str) -> None:
        """Устанавливает self[key] равным value"""
        self._redis.hset(self._hash_name, key, value)

    def __len__(self) -> int:
        """Возвращает количество элементов Hash"""
        return self._redis.hlen(self._hash_name)

    def __getitem__(self, key: str) -> str:
        """Возвращает значение по ключу `key`, если данного ключа нет в Hash, возбуждает KeyError"""
        result: str = self._redis.hget(self._hash_name, key)
        if result is None:
            raise KeyError(f"Данного ключа нет в `словаре` {self._hash_name}")
        else:
            return result

    def __iter__(self) -> Iterator[str]:
        """Возвращает итератор со всеми ключами Hash"""
        return iter(self.keys())


# TODO: можно ли как-то сделать, чтобы не переписывать каждый метод
class CounterHashManager(RedisHashManager):
    """Наследует функционал RedisHashManager, но при это должен возвращать только всегда int,
     и имеет пару дополнительных методов"""

    def increment(self, key: str, amount: int = 1) -> int:
        return self._redis.hincrby(self._hash_name, key, amount=amount)

    def __getitem__(self, item: str) -> int:
        return self.get(item, 0)

    def get(self, item: str, default: int = None) -> Union[int, None]:
        return int(super().get(item, default))

    def get_many(self, *keys: str) -> dict[str, int]:
        response: list = self._redis.hmget(self._hash_name, *keys)
        int_response = [int(value) if value is not None else 0 for value in response]
        return dict(zip(keys, int_response))

    def __iter__(self) -> Iterator[int]:
        return (int(value) for value in super().__iter__())
