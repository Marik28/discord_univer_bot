import re

from discord import Embed

# from bot import connection
from constants import COMMANDS_DESCRIPTION, anime_pics_list
from datetime_helpers import change_ending, WEEK_DAYS
from embed_handlers import create_field_template, create_embed_template
from exceptions import InvalidImageLink
from redis_api import ANIME_LINKS_LIST


def make_help_embed_message() -> Embed:
    """Оформляет набор всех комманд в виде Embed"""
    embed_dict = create_embed_template(title="Список всех команд", description="Сюда можно будет что-нибудь написать")
    for command, description in COMMANDS_DESCRIPTION.items():
        embed_dict["fields"].append(create_field_template(command, description))
    return Embed().from_dict(embed_dict)


def make_embed_day_schedule(day_schedule_data: list, day, parity) -> Embed:
    """Создает Embed на основе данных о расписании на 1 день"""
    day = change_ending(day)
    title = f"Расписание на {day} ({parity})"
    if len(day_schedule_data) == 0:
        description = "Нет пар получается"
        return Embed.from_dict(create_embed_template(title=title, description=description))
    description = "Придумаю что-нибудь"
    embed_dict = create_embed_template(title=title, description=description)
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


def make_embed_week_schedule(week_schedule: list, parity: str) -> Embed:
    """Создает Embed на основе данных о расписании на неделю"""
    embed_dict = create_embed_template(title=f"Расписание на неделю ({parity})",
                                       description="Сюда можно будет что-нибудь написать")
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
        # это надо пофиксить
        teacher_brief_info_field = create_teacher_brief_info(teacher) if teacher else create_field_template("Препод",
                                                                                                            inline=True)
        day_info_field = create_field_template(day.capitalize() if lesson_num == 1 else "-",
                                               "-", inline=True)
        subject_field = create_field_template(f"{lesson_num} пара ({kind}) - {time}", f"{subject['name']}", inline=True)
        embed_dict["fields"].extend([day_info_field, subject_field, teacher_brief_info_field])
        lesson_num += 1


def create_teacher_brief_info(teacher):
    full_name = get_teacher_name(teacher, initials=True)
    return create_field_template(name="Препод", value=full_name, inline=True)


def make_embed_teacher_list(teacher_list) -> Embed:
    embed_dict = create_embed_template("Список преподавателей", "да-да", allow_anime_thumbnail=False)
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
        f"{name} (Кафедра: {department})",
        f"(Должность: {position}). Номер - {phone}, email - {email}. Подробнее - {link}"
    )
    second_field = create_field_template("Что ведет", f"{process_subjects(teacher)}")
    return [first_field, second_field]


def process_subjects(teacher) -> str:
    practic_set = teacher["practic_set"]
    lecture_set = teacher["lecture_set"]
    lab_set = teacher["lab_set"]
    tmp_list = [(practic_set, "Семинары"), (lecture_set, "Лекции"), (lab_set, "Лабы")]
    return '; '.join([create_subj_set_template(*item) for item in tmp_list])


def create_subj_set_template(subj_set, subj_type) -> str:
    if subj_set is None:
        return '-'
    return f"{subj_type}: {', '.join(subj['name'] for subj in subj_set)} \t"


def make_embed_subject_list(subjects_info: list, init_query: str) -> Embed:
    embed_dict = create_embed_template(title="Найденные предметы:")
    if len(subjects_info) == 0:
        embed_dict["description"] = f'По запросу "{init_query}" нет совпадений'
        return Embed.from_dict(embed_dict)
    embed_dict["description"] = f'Найденные предметы по запросу "{init_query}"'
    for subject in subjects_info:
        name = subject["name"]
        of_link = subject["official_playlist_url"]
        my_link = subject["my_playlist_url"]
        links_description = f"Оффициальный - {of_link}. Плейлист работяг - {my_link} "
        title_field = create_field_template(name, inline=True)
        teachers_info_field = process_teachers(subject)
        links_field = create_field_template("Плейлисты", links_description, inline=True)
        embed_dict["fields"].extend([title_field, teachers_info_field, links_field])
    return Embed.from_dict(embed_dict)


def process_teachers(subject):
    lecturer = get_teacher_name(subject["lecturer"], initials=True) if subject["lecturer"] else None
    lab_teacher = get_teacher_name(subject["lab_teacher"], initials=True) if subject["lab_teacher"] else None
    practic_teacher = get_teacher_name(subject["practic_teacher"], initials=True) if subject[
        "practic_teacher"] else None
    txt = f"Лектор: {lecturer}. Практику ведет: {practic_teacher}. Лабы ведет: {lab_teacher}"
    return create_field_template("Преподы", txt, inline=True)


def init_anime_links_list(filename: str, links_list: list) -> None:
    """Добавляет в переданный список ссылки из файла"""
    with open(filename, "r", encoding='utf-8') as file:
        links_list.extend(link.strip() for link in file.readlines())


def add_link_to_list_and_file(link: str) -> None:
    """Осуществляет валидацию ссылки"""
    if not is_valid_image_link(link):
        raise InvalidImageLink("Ссылка не является правильной :( (по крайней мере она не прошла нашу проверку)")
    else:
        if link in anime_pics_list:
            pass
        else:
            anime_pics_list.append(link)
            with open("anime_pics_links.txt", "a", encoding="utf-8") as file:
                file.write(f"\n{link}")


# def add_link_to_redis_and_file(link: str) -> None:
#     if not is_valid_image_link(link):
#         raise InvalidImageLink("Ссылка не является правильной :( (по крайней мере она не прошла нашу проверку)")
#     else:
#         if connection.sismember(ANIME_LINKS_LIST):
#             pass
#         else:
#             connection.sadd(ANIME_LINKS_LIST)
#             with open("anime_pics_links.txt", "a", encoding="utf-8") as file:
#                 file.write(f"\n{link}")


def is_valid_image_link(link: str) -> bool:
    link_pattern = re.compile(r"^(?P<protocol>http|https)://"
                              r"(?P<domain_and_path>[\w/.-]+)"
                              r"(?P<img_extension>\.(png|jpeg|jpg))"
                              r"(?P<smth_else>.+)?$")
    if link_pattern.match(link) is None:
        return False
    else:
        return True
