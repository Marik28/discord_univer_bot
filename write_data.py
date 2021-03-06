from config import BASE_DIR, ANIME_LINKS_SET
from redis_utils import RedisSetManager, get_redis_connection

links_file = BASE_DIR / 'redis_utils' / 'links.txt'


def save_links_to_redis(file_with_links, redis_set: RedisSetManager):
    with open(file_with_links, 'r') as file:
        links = [link.strip() for link in file.readlines()]
    redis_set.update(links)


if __name__ == '__main__':
    conn = get_redis_connection()
    r_manager = RedisSetManager(conn, ANIME_LINKS_SET)
    save_links_to_redis(links_file, r_manager)
    r_manager.close_connection()
