import redis


def init_redis() -> None:
    with open("anime_pics_links.txt", "r", encoding="utf-8") as file:
        links = [link.strip() for link in file.readlines()]
    connection = redis.Redis(host="localhost", port=6379, db=0)
    connection.flushdb()
    connection.sadd("anime_links", *links)
    print(connection.smembers("anime_links"))


init_redis()