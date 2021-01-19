import redis

from constants import ANIME_LINKS_DB

ANIME_LINKS_LIST = "anime_links"


def init_redis(filename: str) -> redis.Redis:
    with open(filename, "r", encoding="utf-8") as file:
        links = [link.strip() for link in file.readlines()]
    connection = redis.Redis(host="localhost", port=6379, db=ANIME_LINKS_DB)
    connection.flushdb()
    connection.sadd(ANIME_LINKS_LIST, *links)
    print(connection.smembers("anime_links"))
    return connection
