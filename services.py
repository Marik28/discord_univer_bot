import datetime as dt
import random
from pprint import pprint

from discord import Embed, Color
import requests

from exceptions import ErrorFromServer, EmptyJsonError


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

    r_json = response.json()
    if response.status_code == 200:
        if len(r_json) > 0:
            return r_json
        else:
            raise EmptyJsonError
    else:
        raise ErrorFromServer(f"Status :{response.status_code}. Message: {response.text}")


def make_embed_day_schedule(day_schedule_data, parity) -> Embed:
    """Создает Embed на основе данных о расписании на 1 день"""
    day = day_schedule_data[0]["day"]["name"]
    embed_dict = {
        "color": Color.blue().value,
        "title": f"Расписание на {day} ({parity})",
        "fields": [],
        "thumbnail": {"url": random.choice(ANIME_PICS_LIST)},
        "description": "Сюда можно будет что-нибудь написать",
    }
    lesson_num = 1
    for lesson in day_schedule_data:
        teacher = lesson['teacher']
        time = lesson["time"]
        subject = lesson["subject"]
        kind = lesson["kind"]["name"]
        teacher_info_field = create_teacher_info_field(teacher)
        subject_field = create_field_template(f"{lesson_num} пара ({kind}) - {time}", f"{subject['name']}")
        embed_dict["fields"].append(subject_field)
        embed_dict["fields"].extend(teacher_info_field)
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
    r_json = response.json()
    if response.status_code == 200:
        if len(r_json) > 0:
            return r_json
        else:
            raise EmptyJsonError
    else:
        raise ErrorFromServer(f"Status: {response.status_code}. Message: {response.text}")


def get_teacher_name(teacher, initials=False) -> str:
    """Возвращает полное имя преподавателя"""
    s_name = teacher["second_name"]
    f_name = teacher["first_name"]
    m_name = teacher["middle_name"]
    if not initials:
        return f"{s_name}, {f_name} {m_name}"
    else:
        return f"{s_name}, {f_name[0]}. {m_name[0]}."


def create_teacher_info_field(teacher) -> list[dict]:
    """Возвращает массив из полей с инфо о преподе для Embed"""
    name = create_field_template(name="Препод", inline=True,
                                 value=get_teacher_name(teacher))
    contact = create_field_template(name="Номер телефона", inline=True,
                                    value=f"{teacher['phone_number'] if teacher['phone_number'] else '-'}",)
    kstu_link = create_field_template(name="Подробнее", inline=True,
                                      value=f"{teacher['kstu_link'] if teacher['kstu_link'] else '-'}")
    return [name, contact, kstu_link]


def create_field_template(name: str, value: str, inline=False) -> dict:
    """Шаблон для создания одного field для Embed"""
    return {
        "name": name,
        "value": value,
        "inline": inline,
    }
