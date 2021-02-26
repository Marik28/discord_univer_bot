from typing import Iterable, Union, Iterator

from redis import Redis

from exceptions import InvalidImageLink
from validators import is_valid_image_link


class RedisSetManager:
    """Класс-обертка для упрощенного управления конкретным множеством в Redis.
    Redis обязательно должен быть инициализирован с `decode_responses=True`.
    Возвращаемые значения автоматически декодируются в str. Ведет себя как встроенный set"""

    def __init__(self, redis_: Redis, set_name: str):
        """Необходимо передать экземпляр Redis `redis` с открытым соединением и имя множества `set_name`,
        которым будем пользоваться. Redis обязательно должен быть инициализирован с `decode_responses=True`."""
        self._redis = redis_
        self._set_name = set_name

    def update(self, values: Iterable) -> None:
        """Добавляет несколько значений во множество"""
        self._redis.sadd(self._set_name, *values)

    def add(self, value: str) -> None:
        """Добавляет значение во множество"""
        self._redis.sadd(self._set_name, value)

    def get_random_value(self) -> Union[str, None]:
        """Возвращает случайное значение из множества. Если множество пустое, возвращает None"""
        return self._redis.srandmember(self._set_name)

    def clear(self) -> None:
        """Удаляет все элементы из множества (равносильно удалению множества из Redis)"""
        self._redis.delete(self._set_name)

    def close_connection(self) -> None:
        """Закрывает соединение с Redis"""
        self._redis.close()

    def pop(self) -> Union[str, None]:
        """Удаляет и возвращает случайное значение из множества. Если множество пустое, возвращает None"""
        return self._redis.spop(self._set_name)

    def discard(self, element: str) -> None:
        """Удаляет из элемент `element` из множества, если он есть там.
        Если его нет во множестве, ничего не делает"""
        self._redis.srem(self._set_name, element)

    def remove(self, element: str) -> None:
        """Удаляет из элемент `element` из множества, если он есть там.
        Если его нет во множестве, возбуждает Key Error"""
        existed: bool = self._redis.srem(self._set_name, element)
        if not existed:
            raise KeyError(f"Элемент {element} отсутсвует во множестве {self._set_name}")

    def __len__(self) -> int:
        """Возвращает количество элементов множества"""
        return self._redis.scard(self._set_name)

    def __iter__(self) -> Iterator[str]:
        """Возвращает итератор со всеми элементами множества"""
        return (elem for elem in self._redis.smembers(self._set_name))

    def __contains__(self, item: str) -> bool:
        """Возвращает True, если `item` является элементом множества, иначе False"""
        return self._redis.sismember(self._set_name, item)

    def __str__(self) -> str:
        """str(self)"""
        return str(set(self._redis.smembers(self._set_name)))


class LinksSetManager(RedisSetManager):

    def add_link(self, link: str, validate: bool = True) -> str:
        """Добавляет ссылку во множество Redis. Возвращает сообщение об успешном добавлении,
        даже если ссылка уже лежала во множестве.
        Если сслыка не валидна, кидает исключение InvaliImageLink"""

        if validate and not is_valid_image_link(link):
            raise InvalidImageLink("Ссылка не является правильной :( (по крайней мере она не прошла нашу проверку)")
        self.add(link)
        return 'Картинка добавлена в базу успешно!'
