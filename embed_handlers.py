import random

from constants import COMMAND_PREFIX, anime_pics_list
# from bot import connection
from redis_api import ANIME_LINKS_LIST


def create_embed_template(title: str = "-", description: str = "-", color=None, allow_anime_thumbnail=True, ) -> dict:
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
        embed_dict["thumbnail"] = {"url": random.choice(anime_pics_list)}
        # embed_dict["thumbnail"] = {"url": connection.srandmember(ANIME_LINKS_LIST).decode()}
    return embed_dict


def create_field_template(name: str = "-", value: str = "-", inline=False) -> dict:
    """Шаблон для создания одного field для Embed"""
    return {
        "name": name,
        "value": value,
        "inline": inline,
    }
