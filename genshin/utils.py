import json
import random
from typing import Union

from config import GENSHIN_CHARACTERS_JSON_DIR

FILLED_STAR = "★"
EMPTY_STAR = "☆"

GOLD_COLOR = 0xFFD700
PURPLE_COLOR = 0x800080
BLUE_COLOR = 0x0F52BA


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

five_stars_list = [5 for i in range(2)]
four_stars_list = [4 for i in range(13)]
three_stars_list = [3 for i in range(85)]
# # two_stars_list = [2 for i in range(28)]
# # one_star_list = [1 for i in range(40)]

# для тестов
# five_stars_list = [5 for i in range(45)]
# four_stars_list = [4 for i in range(45)]
# three_stars_list = [3 for i in range(10)]


all_stars_list = five_stars_list + four_stars_list + three_stars_list
assert len(all_stars_list) == 100

path_to_json = GENSHIN_CHARACTERS_JSON_DIR / "genshin_characters.json"
with open(path_to_json) as file:
    characters_list: list[dict] = json.load(file)


rarity_colors = {
    5: GOLD_COLOR,
    4: PURPLE_COLOR,
    3: BLUE_COLOR,
}


def make_rating_list():
    stars_dict = {}
    for stars in range(4, 6):
        stars_dict[stars] = [char for char in characters_list if char["stars"] == stars]
    return stars_dict


def roll_star() -> int:
    roll = random.choice(all_stars_list)
    return roll


def generate_rating(stars: int) -> str:
    rating = FILLED_STAR * stars
    return f"{rating:{EMPTY_STAR}<5}"


stars_to_chars = make_rating_list()


def roll_character(rolled_star: int) -> dict:
    # rolled_star = roll_star()
    # if rolled_star < 4:
    #     return None
    rolled_character = random.choice(stars_to_chars[rolled_star])
    return rolled_character


def get_rarity_color(stars: int) -> int:
    return rarity_colors[stars]


def get_element(name: str) -> str:
    return elements[name]
