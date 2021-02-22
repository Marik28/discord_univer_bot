from redis import Redis

from config import ANIME_LINKS_DB, ANIME_LINKS_SET
from exceptions import InvalidImageLink
from validators import is_valid_image_link


def decode_string(func):
    """Декоратор для декодирования результата функций, возвращающих bytes, в str """

    def wrapper(*args, **kwargs) -> str:
        result = func(*args, **kwargs).decode()
        if isinstance(result, bytes):
            result.decode()
        return result

    return wrapper


class RedisSetManager:
    """Класс для упрощенного управления конкретным множеством в Redis"""

    def __new__(cls, *args, **kwargs):
        """Синглтон, чтобы было, а шо"""
        if not hasattr(cls, 'instance'):
            cls.instance = super(RedisSetManager, cls).__new__(cls)
        return cls.instance

    def __init__(self, connection: Redis, set_name: str):
        self._connection = connection
        self._set_name = set_name

    def add_values(self, members: list[str]):
        """Добавляет несколько значений во множество"""
        return self._connection.sadd(self._set_name, *members)

    def add_value(self, member: str):
        """Добавляет значение во множество"""
        return self._connection.sadd(self._set_name, member)

    @decode_string
    def get_random_value(self):
        """Возвращает случайную ссылку из множества ссылок"""
        return self._connection.srandmember(self._set_name)

    def clear(self):
        """Очищает множество (== удаляет его)"""
        self._connection.delete(self._set_name)


class LinksSetManager(RedisSetManager):

    def add_link(self, link: str, validate: bool = True) -> str:
        """Добавляет ссылку во множество Redis, возвращает сообщение об успешности добавления.
        Если сслыка не валидна, кидает исключение InvaliImageLink"""

        if validate and not is_valid_image_link(link):
            raise InvalidImageLink("Ссылка не является правильной :( (по крайней мере она не прошла нашу проверку)")

        result: int = self.add_value(link)
        if result == 0:
            msg = 'Картинка уже есть в нашей базе'
        else:
            msg = 'Картинка добавлена в базу успешно!'
        return msg


def get_redis_connection(host="localhost", port=6379, db=ANIME_LINKS_DB) -> Redis:
    return Redis(host=host, port=port, db=db)


redis_conn = get_redis_connection()
links_set_manager = LinksSetManager(redis_conn, ANIME_LINKS_SET)
