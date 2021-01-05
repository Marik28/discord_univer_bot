import datetime as dt
import random
from pprint import pprint

from discord import Embed, Color
import requests

from exceptions import ErrorFromServer

PARITIES = {'числитель', 'знаменатель'}

START_WEEK = 1
BASE_API_URL = 'http://127.0.0.1:8000/api/v1/'

ANIME_PICS_LIST = [
    'https://cdn.myanimelist.net/r/360x360/images/characters/15/384405.jpg?s=a1512f99fe479ad49a1bf1bc8642c00a',
    'https://i.ytimg.com/vi/EXtUR2NhBtg/maxresdefault.jpg',
    'https://i.pinimg.com/originals/75/50/19/75501922405ca964a256af6877ce8710.jpg',
]


def get_week_parity() -> str:
    """Возвращает четность недели в виде строки (числитель/знаменатель)"""
    cur_week = int(dt.date.today().strftime('%W'))
    if cur_week % 2 == 0:
        return 'знаменатель'
    else:
        return 'числитель'


def get_day_schedule(day: str, parity: str):
    """Делает запрос к серверу и получает расписание на день,
    предварительно обработав JSON и приведя его к питонячьему виду.
    Расписание отсортировано по времени проведения пары."""
    day = day.lower().strip()
    parity = parity.lower().strip()
    query = {
        'day_name': day,
        'parity': parity,
    }
    response = requests.get(BASE_API_URL + 'schedule/day/', params=query)
    if response.status_code == 200:
        return sorted(response.json(), key=lambda obj: obj['time'])
    else:
        raise ErrorFromServer(f"Status :{response.status_code}. Message: {response.text}")


def make_beautiful_day_view(day_schedule_data) -> str:
    """Приводит полученное расписание к красивому виду для отправки в виде сообщения"""
    msg_bits = []
    i = 1
    for lesson in day_schedule_data:
        teacher = lesson['teacher']
        time = lesson["time"]
        subject = lesson["subject"]
        kind = lesson["kind"]["name"]
        message_template = f'{i} ПАРА({kind}) - {subject["name"]}\n' \
                           f'ВРЕМЯ - {time}\n' \
                           f'Препод - {teacher["second_name"]}, {teacher["first_name"]}, {teacher["middle_name"]}'

        msg_bits.append(message_template)
        i += 1

    day = day_schedule_data[0]["day"]["name"]
    parity = day_schedule_data[0]["parity"]
    msg_start = f'Расписание на {day} ({parity})\n'
    return msg_start + '\n'.join(msg_bits)


def make_embed_day_schedule(day_schedule_data, parity) -> Embed:
    """Создает Embed на основе данных о расписании на 1 день"""
    day = day_schedule_data[0]["day"]["name"]
    embed_dict = {
        "color": Color.blue().value,
        "title": f"Расписание на {day} ({parity})",
        "fields": [],
        "thumbnail": {"url": random.choice(ANIME_PICS_LIST)},
    }
    lesson_num = 1
    for lesson in day_schedule_data:
        teacher = lesson['teacher']
        time = lesson["time"]
        subject = lesson["subject"]
        kind = lesson["kind"]["name"]
        teacher_info_field = {
            "name": ""
        }
        subject_field = {
            "name": f"{lesson_num} пара ({kind}) - {time}",
            "value": f"{subject['name']}"
        }
        embed_dict["fields"].append(subject_field)
        lesson_num += 1
    return Embed().from_dict(embed_dict)


def get_week_schedule(parity: str):
    """Делает запрос к серверу и получает расписание на неделю,
    предварительно обработав JSON и приведя его к питонячьему виду."""
    parity = parity.lower().strip()
    query = {
        'parity': parity,
    }
    response = requests.get(BASE_API_URL + 'schedule/', params=query)
    if response.status_code == 200:
        return response.json()
    else:
        raise ErrorFromServer(f"Status: {response.status_code}. Message: {response.text}")


def test_embed_features():
    dct = {
        "title": "Тестовый заголовок",
        "color": Color.dark_gold().value,
        "fields": [
            {"name": "11111", "value": "kekwait", "inline": True},
            {"name": "222222222", "value": "dsfdsfsdf", "inline": False},
            {"name": "33333", "value": "sadf23g2d", "inline": True},
            {"name": "444444", "value": "sadf23g2d", "inline": True},
        ]
    }
    embed_obj = Embed().from_dict(dct)
    return embed_obj
