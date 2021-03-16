import json
import random
from typing import Union

from config import GENSHIN_CHARACTERS_JSON_DIR

FILLED_STAR = "★"
EMPTY_STAR = "☆"

GOLD_COLOR = 0xFFD700
PURPLE_COLOR = 0x800080
BLUE_COLOR = 0x0F52BA

rarity_colors = {
    5: GOLD_COLOR,
    4: PURPLE_COLOR,
    3: BLUE_COLOR,
}

elements = {
    "Электро": "⚡",
    "Пиро": "🔥",
    "Анемо": "💨",
    "Крио": "❄",
    "Гидро": "🌊",
    "Гео": "🌎",
}

# 5 звезд   - 2 %
# 4 звезды  - 13 %
# 3 звезды  - 85 %
# сумма     - 100 %

five_stars_list = [5 for _ in range(2)]
four_stars_list = [4 for _ in range(13)]
three_stars_list = [3 for _ in range(85)]

# для тестов
# five_stars_list = [5 for i in range(45)]
# four_stars_list = [4 for i in range(45)]
# three_stars_list = [3 for i in range(10)]


all_stars_list = five_stars_list + four_stars_list + three_stars_list
assert len(all_stars_list) == 100

path_to_json = GENSHIN_CHARACTERS_JSON_DIR / "genshin_characters.json"
with open(path_to_json) as file:
    characters_list: list[dict] = json.load(file)


def make_rating_list():
    stars_dict = {}
    for stars in (4, 5):
        stars_dict[stars] = [char for char in characters_list if char["stars"] == stars]
    return stars_dict


def roll_star() -> int:
    roll = random.choice(all_stars_list)
    return roll


def generate_rating(number_of_stars: int) -> str:
    """Отрисовывет звездочки по 5-звездночной шкале"""
    rating = FILLED_STAR * number_of_stars
    return f"{rating:{EMPTY_STAR}<5}"


stars_to_chars = make_rating_list()


def roll_character(rolled_star: int) -> dict:
    rolled_character = random.choice(stars_to_chars[rolled_star])
    return rolled_character


def get_rarity_color(stars: int) -> int:
    return rarity_colors[stars]


def get_element(name: str) -> str:
    return elements[name]
