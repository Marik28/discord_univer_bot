# TODO
#  с неймингом всё плохо
from redis_utils.redis_set import LinksSetManager


class ImageUrlGenerator:
    """Интерфейс для получения случайной ссылки на картинку"""

    def get_random_image_url(self) -> str:
        raise NotImplementedError()


class RedisImageUrlGenerator(ImageUrlGenerator):
    """Класс, который генерирует случайные ссылки с помощью `LinksSetManager`"""
    def __init__(self, redis_set: LinksSetManager):
        self._redis_set = redis_set

    def get_random_image_url(self) -> str:
        self._redis_set.get_random_value()
