from pathlib import Path


anime_pics_list = []

ANIME_LINKS_DB = 0

BASE_DIR = Path.cwd()
ANIME_LINKS_FILE = BASE_DIR / "anime_pics_links.txt"


COMMAND_PREFIX = '!'

COMMANDS_DESCRIPTION = {
    f"{COMMAND_PREFIX}расписание [день] <числитель/знаменатель>":
        "Узнать расписание на 1 день. Вместо дня можно написать 'сегодня/завтра' Если четность недели не указана, "
        "будет выбран день текущей недели",
    f"{COMMAND_PREFIX}неделя <числитель/знаменатель>":
        "Узнать расписание на неделю. Если не указана четность недели, будет выбрана текущая неделя",
    f"{COMMAND_PREFIX}препод/преподы/преподаватель/преподаватели [имя/фимилия/отчество] ":
        "Подробная информация о данном преподе/преподах в нашей БД",
    f"{COMMAND_PREFIX}предмет/предметы [название предмета/часть названия предмета]":
        "Подробная инфа о данном предмете/предметах в нашей БД",
    f"{COMMAND_PREFIX}добавить/addlink [ссылка на картинку]": "Добавляет картинку в список картинок.",
}

ERROR_MSG_BIT = f"Напиши {COMMAND_PREFIX}info, чтобы узнать подробнее о командах бота."
