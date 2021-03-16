import random
from typing import Union

from discord import Embed

from config import COMMAND_PREFIX
from genshin.utils import get_rarity_color, generate_rating, get_element
from models.user_statistics import UserStatistics
from new_embed.models import MyEmbed


def make_genshin_card(user_name: str, rolled_character: Union[dict, None],
                      rarity: int, user_statistics: UserStatistics) -> Embed:
    """Создает карточку с результатом ролла гачи"""
    embed = MyEmbed()

    title = f"Результат ролла {user_name}"
    rolls_info = f"Всего роллов - {user_statistics.total} \n" \
                 f"5-звездочные - {user_statistics.five} \n" \
                 f"4-звездочные - {user_statistics.four} \n" \
                 f"3-звездочные - {user_statistics.three} "

    color = get_rarity_color(rarity)
    stars = generate_rating(rarity)

    embed.color = color
    embed.title = title

    if rarity < 4:
        description = f"Твой ролл - {stars} \n" \
                      f"Ну не везёт получается. {rolls_info} "
        embed.description = description
        return embed
    else:
        description = f"Получается везёт. {rolls_info}"

    embed.description = description
    embed.add_field(name="Редкость", value=stars)

    element = get_element(rolled_character["gods_eye"])
    embed.add_field(name="Имя", value=f"{rolled_character['name']} {element}")

    image_url = random.choice(rolled_character["images"])
    embed.set_image(url=image_url)

    return embed


def create_default_template(title: str = "-", description: str = "-", color=None, random_color: bool = False,
                            random_thumbnail=True, random_image=False) -> Embed:
    """Создает шаблон для Embed"""
    embed = MyEmbed()
    embed.title = title
    embed.description = description

    if random_color:
        embed.color = random.randint(0, 0xFFFFFF)
    elif color is not None:
        embed.color = color

    if random_thumbnail:
        embed.set_thumbnail(url=embed.generate_random_image_link())

    if random_image:
        embed.set_image(url=embed.generate_random_image_link())

    embed.set_footer(text=f"Напиши {COMMAND_PREFIX}info, чтобы узнать список команд")

    return embed
