import random

from discord import Embed

from constants import COMMAND_PREFIX
from redis_utils.redis_api import get_random_link


def create_embed_template(title: str = "-", description: str = "-", color=None, allow_anime_thumbnail=True,
                          allow_image=False) -> dict:
    """Создает шаблон для Embed"""
    embed_dict = {
        "title": title,
        "fields": [],
        "description": description,
        "footer": {
            "text": f"Напиши {COMMAND_PREFIX}info, чтобы узнать список команд",
        },
    }
    if color is not None:
        embed_dict["color"] = color
    else:
        embed_dict["color"] = random.randint(0, 0xFFFFFF)
    if allow_anime_thumbnail:
        embed_dict["thumbnail"] = {"url": get_random_link()}
    if allow_image:
        embed_dict["image"] = {"url": get_random_link()}
    return embed_dict


def create_field_template(name: str = "-", value: str = "-", inline=False) -> dict:
    """Шаблон для создания одного field для Embed"""
    return {
        "name": name,
        "value": value,
        "inline": inline,
    }


def make_embed_image() -> Embed:
    """Создает Embed для отправки картинки"""
    embed = create_embed_template(title="Картиночка", description="Вот тебе картиночка",
                                  allow_anime_thumbnail=False, allow_image=True)
    return Embed.from_dict(embed)
