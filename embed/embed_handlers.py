import random
from typing import Union

from discord import Embed

from config import COMMAND_PREFIX
from genshin.utils import generate_rating, get_rarity_color, get_element
from redis_utils import links_set_manager

from .basic_embed_funcs import create_field_template, create_media_object_template


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
        # embed_dict["thumbnail"] = {"url": get_random_link()}
        embed_dict["thumbnail"] = {"url": links_set_manager.get_random_value()}
    if allow_image:
        embed_dict["image"] = {"url": links_set_manager.get_random_value()}
        # embed_dict["image"] = {"url": random.choice(anime_pics_list)}
    return embed_dict


def make_embed_image() -> Embed:
    """Создает Embed для отправки картинки"""
    embed = create_embed_template(title="Картиночка", description="Вот тебе картиночка",
                                  allow_anime_thumbnail=False, allow_image=True)
    return Embed.from_dict(embed)


def make_genshin_card(user_name: str, rolled_character: Union[dict, None], rarity: int, user_rolls_count: int) -> Embed:
    """Создает карточку с результатом ролла гачи"""

    title = f"Результат ролла {user_name}"
    rolls_info = f"Всего роллов - {user_rolls_count}"
    color = get_rarity_color(rarity)
    stars = generate_rating(rarity)
    if rarity < 4:
        description = f"Ну не везёт получается. {rolls_info} \n {stars}"
        return Embed.from_dict(create_embed_template(title=title, description=description, color=color,
                                                     allow_anime_thumbnail=False))
    else:
        description = f"Получается везёт. {rolls_info}"

    embed = create_embed_template(title=title, description=description, color=color, allow_anime_thumbnail=False)
    rating_field = create_field_template(name="Редкость", value=f"{stars}")
    embed["fields"].append(rating_field)

    element = get_element(rolled_character["gods_eye"])
    name_field = create_field_template(name="Имя", value=f"{rolled_character['name']} {element}")
    embed["fields"].append(name_field)

    image_url = random.choice(rolled_character["images"])
    image = create_media_object_template(url=image_url)
    embed["image"] = image

    return Embed.from_dict(embed)
