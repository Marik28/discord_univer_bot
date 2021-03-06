import random
from typing import Union

from discord import Embed

from genshin.utils import get_rarity_color, generate_rating, get_element
from models import redis_links_generator
from models.user_statistics import UserStatistics
from new_embed.models import MyEmbed


def make_genshin_card(user_name: str, rolled_character: Union[dict, None], rarity: int, user_statistics: UserStatistics) -> Embed:
    """Создает карточку с результатом ролла гачи"""
    embed = MyEmbed(redis_links_generator)

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
