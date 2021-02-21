from config import BASE_DIR, ANIME_LINKS_SET
from redis_utils import redis_api

links_file = BASE_DIR / 'redis_utils' / 'links.txt'


def save_links_to_redis(file_with_links, manager: redis_api.RedisSetManager):
    with open(file_with_links, 'r') as file:
        links = [link.strip() for link in file.readlines()]
    manager.add_values(links)


if __name__ == '__main__':
    conn = redis_api.get_redis_connection()
    r_manager = redis_api.RedisSetManager(conn, ANIME_LINKS_SET)
    save_links_to_redis(links_file, r_manager)
