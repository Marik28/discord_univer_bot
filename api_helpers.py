import requests
from requests import Response

from exceptions import EmptyJson, ErrorFromServer

BASE_API_URL = 'http://127.0.0.1:8000/api/v1/'


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
    if successful_request(response):
        if len(r_json) > 0:
            return r_json
        else:
            raise EmptyJson
    else:
        msg = get_error_msg_template(response)
        raise ErrorFromServer(msg)


def get_week_schedule(parity: str):
    """Делает запрос к серверу и получает расписание на неделю,
    предварительно обработав JSON и приведя его к питонячьему виду."""
    parity = parity.lower().strip()
    query = {
        'parity': parity,
    }
    response = requests.get(BASE_API_URL + 'schedule/', params=query)
    r_json = response.json()
    if successful_request(response):
        return r_json
    else:
        msg = get_error_msg_template(response)
        raise ErrorFromServer(msg)


def get_teacher_list(arg):
    """Делает запрос к серверу и получает список преподов,
    предварительно обработав JSON и приведя его к питонячьему виду."""
    if arg is None:
        arg = ''
    query = {
        "q": arg,
    }
    response = requests.get(BASE_API_URL + 'teachers/filter/', params=query)
    if successful_request(response):
        return response.json()
    else:
        msg = get_error_msg_template(response)
        raise ErrorFromServer(msg)


def successful_request(response: Response) -> bool:
    return response.status_code == 200


def get_error_msg_template(response: Response) -> str:
    return f"Status: {response.status_code}. Message: {response.text}"