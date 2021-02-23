import os
from pathlib import Path

# всё, что нужно для бота

API_TOKEN = os.getenv('DISCORD_BOT_API_TOKEN')

# параметры для взаимодействия с сервером REST API
# BASE_API_URL = 'http://marik28.pythonanywhere.com/api/v1/'
BASE_API_URL = os.getenv("BASE_API_URL")

# команды и прочее

# COMMAND_PREFIX = '.'
COMMAND_PREFIX = os.getenv("COMMAND_PREFIX", ".")

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
    f"{COMMAND_PREFIX}картинка/аниме": "Показывает рандомную аниме пикчу из нашей базы",
}

ERROR_MSG_BIT = f"Напиши {COMMAND_PREFIX}info, чтобы узнать подробнее о командах бота."


# директории

BASE_DIR = Path.cwd()

# переменные, связанные с Redis

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
ANIME_LINKS_DB = int(os.getenv("ANIME_LINKS_DB", "0"))
ANIME_LINKS_SET = os.getenv("ANIME_LINKS_SET", "anime_links")
TEST_DB = 1
