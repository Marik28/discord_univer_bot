import random
from typing import Union

from discord import Embed


from config import COMMAND_PREFIX
from genshin.utils import generate_rating
from redis_utils import links_set_manager


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


def make_genshin_card(user_name: str, rolled_character: Union[dict, None], user_rolls_count: int) -> Embed:
    is_character = rolled_character is not None
    title = f"Результат ролла {user_name}"
    rolls_info = f"Всего роллов - {user_rolls_count}"
    if not is_character:
        description = f"Не везет получается. {rolls_info}"
        return Embed.from_dict(create_embed_template(title=title, description=description, allow_anime_thumbnail=False))
    description = f"Тебе выпал персонаж!!!. Всего роллов - {rolls_info}"

    embed = create_embed_template(title=title, description=description, allow_anime_thumbnail=False)

    stars = generate_rating(rolled_character['stars'])
    rating_field = create_field_template(name="Редкость", value=f"{stars}", inline=False)
    embed["fields"].append(rating_field)

    name_field = create_field_template(name="Имя", value=f"{rolled_character['name']}")
    embed["fields"].append(name_field)

    embed["image"] = {"url": random.choice(rolled_character["images"])}

    return Embed.from_dict(embed)
