import aiohttp
from aiohttp import ClientConnectorError

from exceptions import ErrorFromServer

BASE_API_URL = 'http://marik28.pythonanywhere.com/api/v1/'


async def handle_request(endpoint: str, query=None):
    """Корутина, делающая GET-запрос на переданный endpoint. В случае успеха возвращает распаршенный (?) JSON ответа.
    Если на сервере произошла ошибка, возвращает её текст."""
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(BASE_API_URL + endpoint, params=query) as response:
                if response.status == 200:
                    r_json = await response.json()
                    return r_json
                else:
                    r_text = await response.text()
                    msg = get_error_msg_template(response.status, r_text)
                    raise ErrorFromServer(msg)
        except ClientConnectorError as e:
            raise ErrorFromServer(str(e))


async def get_day_schedule(day: str, parity: str):
    """Делает запрос к серверу и получает расписание на день,
    предварительно обработав JSON и приведя его к питонячьему виду.
    Расписание отсортировано по времени проведения пары."""
    day = day.lower().strip()
    parity = parity.lower().strip()
    query = {
        'day_name': day,
        'parity': parity,
    }
    r_json = await handle_request('schedule/day/', query=query)
    return r_json


async def get_week_schedule(parity: str):
    """Делает запрос к серверу и получает расписание на неделю,
    предварительно обработав JSON и приведя его к питонячьему виду."""
    parity = parity.lower().strip()
    query = {
        'parity': parity,
    }
    r_json = await handle_request("schedule/", query)
    return r_json


async def get_teacher_list(arg):
    """Делает запрос к серверу и получает список преподов на основе переданного аргумента,
    предварительно обработав JSON и приведя его к питонячьему виду."""
    query = {
        "q": arg,
    }
    r_json = await handle_request('teachers/filter/', query)
    return r_json


async def get_subject_list(arg):
    """Делает запрос к серверу и получает отфильтрованный список предметов
    исходя из переданного аргумента"""
    if arg is not None:
        query = {
            "q": arg,
        }
    else:
        query = None
    r_json = await handle_request('subjects/filter/', query)
    return r_json


def get_error_msg_template(r_status: int, r_text: str) -> str:
    return f"Сервер вернул ошибку {r_status}: '{r_text}'"
