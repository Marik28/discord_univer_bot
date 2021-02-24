from typing import Iterable, Union

from redis import Redis

from config import ANIME_LINKS_DB, ANIME_LINKS_SET, REDIS_PORT, REDIS_HOST
from exceptions import InvalidImageLink
from validators import is_valid_image_link


# не знаю, нужно ли это пока что
# class BaseRedisCollectionManager:
#     """Базовый класс для управления коллекциями Redis"""
#     def __init__(self, connection: Redis):
#         self._connection = connection
#
#     def close_connection(self):
#         """Закрывает соединение с Redis"""
#         self._connection.close()


class RedisSetManager:
    """Класс-обертка для упрощенного управления конкретным множеством в Redis.
    Возвращаемые значения автоматически декодируются в str"""

    def __init__(self, connection: Redis, set_name: str):
        self._connection = connection
        self._set_name = set_name

    def update(self, values: Iterable) -> None:
        """Добавляет несколько значений во множество"""
        self._connection.sadd(self._set_name, *values)

    def add(self, value: str) -> None:
        """Добавляет значение во множество"""
        self._connection.sadd(self._set_name, value)

    def get_random_value(self) -> Union[str, None]:
        """Возвращает случайное значение из множества. Если множество пустое, возвращает None"""
        random_value: bytes = self._connection.srandmember(self._set_name)
        if random_value is None:
            return random_value
        else:
            return random_value.decode()

    def clear(self):
        """Очищает множество (== удаляет его)"""
        self._connection.delete(self._set_name)

    def close_connection(self):
        """Закрывает соединение с Redis"""
        self._connection.close()

    def pop(self) -> Union[str, None]:
        """Удаляет и возвращает случайное значение из множества. Если множество пустое, возвращает None"""
        random_value: bytes = self._connection.spop(self._set_name)
        if random_value is None:
            return random_value
        else:
            return random_value.decode()

    def discard(self, value: str):
        """Удаляет из элемент из множества, если он есть там"""
        self._connection.srem(self._set_name, value)

    def __len__(self):
        """Возвращает количество элементов множества"""
        return self._connection.scard(self._set_name)

    def __iter__(self):
        """Возвращает итератор со всеми элементами множества"""
        all_elements = self._connection.smembers(self._set_name)
        return (elem.decode() for elem in all_elements)

    def __contains__(self, item: str):
        return self._connection.sismember(self._set_name, item)


class LinksSetManager(RedisSetManager):

    def add_link(self, link: str, validate: bool = True) -> str:
        """Добавляет ссылку во множество Redis. Возвращает сообщение об успешном добавлении,
        даже если ссылка уже лежала во множестве.
        Если сслыка не валидна, кидает исключение InvaliImageLink"""

        if validate and not is_valid_image_link(link):
            raise InvalidImageLink("Ссылка не является правильной :( (по крайней мере она не прошла нашу проверку)")
        self.add(link)
        return 'Картинка добавлена в базу успешно!'


def get_redis_connection(host=REDIS_HOST, port=REDIS_PORT, db=0) -> Redis:
    return Redis(host=host, port=port, db=db)


redis_conn = get_redis_connection(db=ANIME_LINKS_DB)
links_set_manager = LinksSetManager(redis_conn, ANIME_LINKS_SET)
