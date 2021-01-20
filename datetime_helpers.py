import datetime as dt

DAY_SPECIAL_WORDS = {"сегодня", "завтра"}

START_WEEK = int(dt.date(year=2021, month=1, day=18).strftime('%W'))

WEEK_DAYS = (
    "понедельник",
    "вторник",
    "среда",
    "четверг",
    "пятница",
    "суббота",
    "воскресенье"
)

INT_TO_WEEK_DAYS = {i: WEEK_DAYS[i] for i in range(len(WEEK_DAYS))}

ENDINGS = {
    "понедельник": "понедельник",
    "вторник": "вторник",
    "среда": "среду",
    "четверг": "четверг",
    "пятница": "пятницу",
    "суббота": "субботу",
    "воскресенье": "воскресенье",
}


def get_week_parity() -> str:
    """Возвращает четность недели в виде строки (числитель/знаменатель)"""
    cur_week = int(dt.date.today().strftime('%W'))
    if cur_week % 2 == 1:
        return 'числитель'
    else:
        return 'знаменатель'


def change_ending(day: str) -> str:
    return ENDINGS[day]


def get_tomorrow_day() -> str:
    today = dt.date.today().weekday()
    return INT_TO_WEEK_DAYS[today + 1 if today <= 6 else 0]


def get_today_day() -> str:
    today = dt.date.today().weekday()
    return INT_TO_WEEK_DAYS[today]


from_word_to_day = {
    "сегодня": get_today_day,
    "завтра": get_tomorrow_day,
}
