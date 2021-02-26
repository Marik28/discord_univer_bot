import json
import random
from typing import Union

from config import GENSHIN_CHARACTERS_JSON_DIR

FILLED_STAR = "★"
EMPTY_STAR = "☆"

# 5 звезд   - 2 %
# 4 звезды  - 10 %
# 3 звезды  - 20 %
# 2 звезды  - 28 %
# 1 звезда  - 40 %
# сумма     - 100 %

five_stars_list = [5 for i in range(2)]
four_stars_list = [4 for i in range(10)]
three_stars_list = [3 for i in range(20)]
two_stars_list = [2 for i in range(28)]
one_star_list = [1 for i in range(40)]

all_stars_list = five_stars_list + four_stars_list + three_stars_list + two_stars_list + one_star_list
assert len(all_stars_list) == 100

path_to_json = GENSHIN_CHARACTERS_JSON_DIR / "genshin_characters.json"
with open(path_to_json) as file:
    characters_list: list[dict] = json.load(file)


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


def roll_character() -> Union[dict, None]:
    rolled_star = roll_star()
    if rolled_star < 4:
        return None
    rolled_character = random.choice(stars_to_chars[rolled_star])
    return rolled_character
