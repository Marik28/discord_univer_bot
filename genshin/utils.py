import random

FILLED_STAR = "★"
EMPTY_STAR = "☆"

# 5 звезд   - 1 %
# 4 звезды  - 4 %
# 3 звезды  - 15 %
# 2 звезды  - 30 %
# 1 звезда  - 50 %
# сумма     - 100 %

five_stars_list = [5]
four_stars_list = [4 for i in range(4)]
three_stars_list = [3 for i in range(15)]
two_stars_list = [2 for i in range(30)]
one_star_list = [1 for i in range(50)]

all_stars_list = five_stars_list + four_stars_list + three_stars_list + two_stars_list + one_star_list
assert len(all_stars_list) == 100


def roll_star() -> int:
    roll = random.choice(all_stars_list)
    print(roll)
    return roll


def generate_rating(stars: int) -> str:
    rating = FILLED_STAR * stars
    return f"{rating:{EMPTY_STAR}<5}"


print(generate_rating(roll_star()))

