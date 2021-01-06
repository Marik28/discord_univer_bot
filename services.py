import datetime as dt
import random

from discord import Embed, Color

from init import COMMANDS_DESCRIPTION, COMMAND_PREFIX, ANIME_PICS_LIST, WEEK_DAYS, ENDINGS


def make_help_embed_message() -> Embed:
    """Оформляет набор всех комманд в виде Embed"""

    embed_dict = create_embed_template(title="Список всех команд", description="Сюда можно будет что-нибудь написать",
                                       color=Color.blue().value)
    for command in COMMANDS_DESCRIPTION:
        embed_dict["fields"].append(create_field_template(command[0], command[1]))
    return Embed().from_dict(embed_dict)


def create_embed_template(title, description, color=None, allow_anime_thumbnail=True, ) -> dict:
    """Создает шаблон для Embed"""
    embed_dict = {
        "title": title,
        "fields": [],
        "description": description,
        "footer": {
            "text": f"Напиши {COMMAND_PREFIX}info, чтобы узнать список команд",
        },
    }
    if color is not None:
        embed_dict["color"] = color
    if allow_anime_thumbnail:
        embed_dict["thumbnail"] = {"url": random.choice(ANIME_PICS_LIST)}
    return embed_dict


def get_week_parity() -> str:
    """Возвращает четность недели в виде строки (числитель/знаменатель)"""
    cur_week = int(dt.date.today().strftime('%W'))
    if cur_week % 2 == 0:
        return 'числитель'
    else:
        return 'знаменатель'


def make_embed_day_schedule(day_schedule_data: list, parity) -> Embed:
    """Создает Embed на основе данных о расписании на 1 день"""
    day = change_ending(day_schedule_data[0]["day"]["name"])
    embed_dict = create_embed_template(title=f"Расписание на {day} ({parity})",
                                       description="Сюда можно будет что-нибудь написать",
                                       color=Color.blue().value)
    lesson_num = 1
    for lesson in day_schedule_data:
        teacher = lesson['teacher']
        time = lesson["time"]
        subject = lesson["subject"]
        kind = lesson["kind"]["name"]
        teacher_info_field = create_teacher_info_fields(teacher)
        subject_field = create_field_template(f"{lesson_num} пара ({kind}) - {time}", f"{subject['name']}")
        embed_dict["fields"].append(subject_field)
        embed_dict["fields"].extend(teacher_info_field)
        lesson_num += 1
    return Embed().from_dict(embed_dict)


def change_ending(day: str) -> str:
    return ENDINGS[day]


def get_teacher_name(teacher, initials=False) -> str:
    """Возвращает полное имя преподавателя"""
    s_name = teacher["second_name"]
    f_name = teacher["first_name"]
    m_name = teacher["middle_name"]
    if not initials:
        return f"{s_name}, {f_name} {m_name}"
    else:
        return f"{s_name}, {f_name[0]}. {m_name[0]}."


def create_teacher_info_fields(teacher) -> list[dict]:
    """Возвращает массив из полей с инфо о преподе для Embed"""
    name = create_field_template(name="Препод", inline=True,
                                 value=get_teacher_name(teacher))
    contact = create_field_template(name="Номер телефона", inline=True,
                                    value=f"{teacher['phone_number'] if teacher['phone_number'] else '-'}", )
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


def make_embed_week_schedule(week_schedule: list, parity: str) -> Embed:
    """Создает Embed на основе данных о расписании на неделю"""
    embed_dict = create_embed_template(title=f"Расписание на неделю ({parity})",
                                       description="Сюда можно будет что-нибудь написать",
                                       color=Color.blue().value)
    for day in WEEK_DAYS:
        cur_lessons = [lesson for lesson in week_schedule if lesson["day"]["name"] == day]
        if len(cur_lessons) > 0:
            add_day_info(sorted(cur_lessons, key=lambda les: les["time"]), embed_dict, day)
    return Embed.from_dict(embed_dict)


def add_day_info(lessons: list, embed_dict: dict, day: str) -> None:
    lesson_num = 1
    for lesson in lessons:
        teacher = lesson['teacher']
        time = lesson["time"]
        subject = lesson["subject"]
        kind = lesson["kind"]["name"]
        teacher_brief_info_field = create_teacher_brief_info(teacher)
        day_info_field = create_field_template(day.capitalize() if lesson_num == 1 else "-",
                                               "-", inline=True)
        subject_field = create_field_template(f"{lesson_num} пара ({kind}) - {time}", f"{subject['name']}", inline=True)
        embed_dict["fields"].extend([day_info_field, subject_field, teacher_brief_info_field])
        lesson_num += 1


def create_teacher_brief_info(teacher):
    full_name = get_teacher_name(teacher, initials=True)
    return create_field_template(name="Препод", value=full_name, inline=True)


def make_embed_teacher_list(teacher_list) -> Embed:
    embed_dict = create_embed_template("Список преподавателей", "да-да")
    for teacher in teacher_list:
        fields = make_detail_teacher_fields(teacher)
        embed_dict["fields"].extend(fields)
    return Embed.from_dict(embed_dict)


def make_detail_teacher_fields(teacher) -> list:
    name = get_teacher_name(teacher)
    email = teacher["email"]
    phone = teacher["phone_number"]
    department = teacher["department"]["name"] if teacher["department"] else None
    position = teacher["position"]
    link = teacher["kstu_link"]
    first_field = create_field_template(
        f"{name} ({department})", f"({position}). Номер - {phone}, email - {email}. Подробнее - {link}"
    )
    second_field = create_field_template("Что ведет", f"{process_subjects(teacher)}")
    return [first_field, second_field]


def process_subjects(teacher) -> str:
    practic_set = teacher["practic_set"]
    lecture_set = teacher["lecture_set"]
    lab_set = teacher["lab_set"]
    tmp_list = [(practic_set, "Семинары"), (lecture_set, "Лекции"), (lab_set, "Лабы")]
    return '; '.join([create_subj_set_template(*item)for item in tmp_list])


def create_subj_set_template(subj_set, subj_type) -> str:
    if subj_set is None:
        return '-'
    return f"{subj_type}: {', '.join(subj['name'] for subj in subj_set)} \t"
