# TODO
#  опять же плохой нейминг
import random

from discord import Embed

from config import COMMAND_PREFIX
from models.random_image_url_generators import ImageUrlGenerator


class MyEmbed(Embed):
    """Расширяет стандартный Embed дополнительными методами для создания шаблонов"""

    def __init__(self, links_generator: ImageUrlGenerator):
        super().__init__()
        self._links_generator = links_generator

    def generate_random_image_link(self) -> str:
        return self._links_generator.get_random_image_url()

    def create_default_template(self, title: str = "-", description: str = "-", color=None, random_color: bool = False,
                                random_thumbnail=True, random_image=False) -> Embed:
        """Создает шаблон для Embed"""
        self.title = title
        self.description = description

        if random_color:
            self.color = random.randint(0, 0xFFFFFF)
        elif color is not None:
            self.color = color

        if random_thumbnail:
            self.set_thumbnail(url=self.generate_random_image_link())

        if random_image:
            self.set_image(url=self.generate_random_image_link())

        self.set_footer(text=f"Напиши {COMMAND_PREFIX}info, чтобы узнать список команд")

        return self
