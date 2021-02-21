import redis

from config import ANIME_LINKS_DB, ANIME_LINKS_SET
from exceptions import InvalidImageLink
from validators import is_valid_image_link


def decode_string(func):
    """Декоратор для декодирования результата функций, возвращающих bytes, в str """
    def wrapper(*args, **kwargs) -> str:
        return func(*args, **kwargs).decode()

    return wrapper


class RedisManager:
    """Класс для упрощенного управления БД Redis"""

    def __init__(self, connection: redis.Redis, links_set_name: str = None):
        self._connection = connection
        self._links_set_name = links_set_name

    def add_link_to_set(self, link: str) -> str:
        """Добавляет ссылку во множество Redis, возвращает сообщение об успешности добавления.
        Если сслыка не валидна, кидает исключение InvaliImageLink"""

        if not is_valid_image_link(link):
            raise InvalidImageLink("Ссылка не является правильной :( (по крайней мере она не прошла нашу проверку)")
        else:
            if self._connection.sismember(self._links_set_name, link):
                msg = 'Картинка уже есть в нашей базе'
            else:
                self._connection.sadd(self._links_set_name, link)
                msg = 'Картинка добавлена в базу успешно!'
        return msg

    @decode_string
    def get_random_link(self):
        """Возвращает случайную ссылку из множества ссылок"""
        return self._connection.srandmember(self._links_set_name)


def get_redis_connection(host="localhost", port=6379, db=ANIME_LINKS_DB) -> redis.Redis:
    connection = redis.Redis(host=host, port=port, db=db)
    return connection


redis_conn = get_redis_connection()
