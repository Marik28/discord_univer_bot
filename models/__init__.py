from redis_utils import links_set_manager

from .random_image_url_generators import RedisImageUrlGenerator


redis_links_generator = RedisImageUrlGenerator(links_set_manager)
