# TODO
#  опять же плохой нейминг

from discord import Embed

from models import redis_links_generator
from models.random_image_url_generators import ImageUrlGenerator


class MyBaseEmbed(Embed):
    """Расширяет стандартный Embed. Предоставляет дополнительный метод для генерации рандомных картинок"""

    _links_generator: ImageUrlGenerator = None

    def generate_random_image_link(self) -> str:
        return self._links_generator.get_random_image_url()


class MyEmbed(MyBaseEmbed):
    """В качестве генератора пикч использует RedisImageUrlGenerator"""
    _links_generator: ImageUrlGenerator = redis_links_generator
