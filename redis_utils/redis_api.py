import redis

from constants import ANIME_LINKS_DB, ANIME_LINKS_FILE
from exceptions import InvalidImageLink
from validators import is_valid_image_link

ANIME_LINKS_LIST = "anime_links"


def init_redis(filename: str) -> redis.Redis:
    with open(filename, "r", encoding="utf-8") as file:
        links = [link.strip() for link in file.readlines()]
    connection = redis.Redis(host="localhost", port=6379, db=ANIME_LINKS_DB)
    connection.flushdb()
    connection.sadd(ANIME_LINKS_LIST, *links)
    return connection


connection = init_redis(ANIME_LINKS_FILE)


def add_link_to_redis(link: str) -> str:
    if not is_valid_image_link(link):
        raise InvalidImageLink("Ссылка не является правильной :( (по крайней мере она не прошла нашу проверку)")
    else:
        if connection.sismember(ANIME_LINKS_LIST, link):
            msg = 'Картинка уже есть в нашей базе'
        else:
            connection.sadd(ANIME_LINKS_LIST, link)
            with open(ANIME_LINKS_FILE, "a", encoding="utf-8") as file:
                file.write(f"\n{link}")
                msg = 'Картинка добавлена в базу успешно!'
    return msg


def get_random_link() -> str:
    return connection.srandmember(ANIME_LINKS_LIST).decode()
