import aiohttp
from aiohttp import ClientResponse

from exceptions import ErrorFromServer

BASE_API_URL = 'http://127.0.0.1:8000/api/v1/'


async def handle_request(endpoint: str, query=None):
    """Корутина, делающая запрос на переданный endpoint"""
    async with aiohttp.ClientSession() as session:
        async with session.get(BASE_API_URL + endpoint, params=query) as response:
            if response.status == 200:
                r_json = await response.json()
                return r_json
            else:
                msg = get_error_msg_template(response)
                raise ErrorFromServer(msg)


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
    """Делает запрос к серверу и получает отфильтрованный список предметов исходя из переданного аргумента"""
    query = {
        "q": arg,
    }
    r_json = await handle_request('subjects/filter/', query)
    return r_json


def get_error_msg_template(response: ClientResponse) -> str:
    return f"Сервер вернул ошибку {response.status}"
