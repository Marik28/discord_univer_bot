from discord.ext import commands
from discord.ext.commands import Context

import config
from api_helpers import get_teacher_list, get_day_schedule, get_week_schedule, get_subject_list
from exceptions import ErrorFromServer, InvalidImageLink
from constants import COMMAND_PREFIX, anime_pics_list, ERROR_MSG_BIT
from services import get_week_parity, make_embed_day_schedule, make_embed_week_schedule, make_help_embed_message, \
    make_embed_teacher_list, make_embed_subject_list, init_anime_links_list, add_link_to_list_and_file

bot = commands.Bot(command_prefix=COMMAND_PREFIX)


@bot.event
async def on_ready():
    print('Бот подключился к серверу')


@bot.command(name='hello')
async def hello(ctx: Context):
    await ctx.send('Дарова, чел')


@bot.command(aliases=['расписание', 'пары'])
async def process_day_schedule_command(ctx: Context, day: str = None, parity=None):
    """Узнает расписание на конкретный день недели. Если не указана четность недели, берется четность текущей недели
    Результат отправляет в виде Embed-сообщения"""
    if day is None:
        msg = f"Нужно указать хотя бы день недели, на который узнает расписание.{ERROR_MSG_BIT}"
    else:
        if parity is None:
            parity = get_week_parity()
        try:
            raw_day_schedule = await get_day_schedule(day, parity)
        except ErrorFromServer as e:
            msg = str(e)
        except ConnectionRefusedError:
            msg = "Не удалось подключиться к серверу"
        else:
            await ctx.send(embed=make_embed_day_schedule(raw_day_schedule, day, parity))
            return
    await ctx.send(msg)


@bot.command(name='неделя')
async def process_week_schedule_command(ctx: Context, parity=None):
    """Узнает расписание на целую неделю. Если не указана четность недели, берется четность текущей недели.
    Результат отправляет в виде Embed-сообщения"""
    if parity is None:
        parity = get_week_parity()
    try:
        raw_week_schedule = await get_week_schedule(parity)
    except ErrorFromServer as e:
        await ctx.send(str(e))
    else:
        await ctx.send(embed=make_embed_week_schedule(raw_week_schedule, parity))


@bot.command(name='info')
async def process_test_command(ctx: Context):
    """Отправляет Embed-сообщение со списком команд и их описанием"""
    await ctx.send(embed=make_help_embed_message())


@bot.command(aliases=['препод', 'преподы'])
async def process_teacher_command(ctx: Context, arg=None):
    """Производит поиск по преподам на совпадение Ф./И./О. препода.
    Возвращает список совпадений в виде Embed-сообщения"""
    if arg is None:
        msg = f"Небходимо написать имя/фамилию/отчество препода. {ERROR_MSG_BIT}"
    else:
        try:
            raw_teachers_info = await get_teacher_list(arg)
        except ErrorFromServer as e:
            msg = str(e)
        else:
            await ctx.send(embed=make_embed_teacher_list(raw_teachers_info))
            return
    await ctx.send(msg)


@bot.command(aliases=['предмет', 'предметы'])
async def process_subjects_command(ctx: Context, arg=None):
    """Производит поиск по предметам на совпадение части названия.
    Возвращает список совпадений в виде Embed-сообщения"""
    if arg is None:
        msg = f"Небходимо написать хотя бы часть названия предмета. {ERROR_MSG_BIT}"
    else:
        try:
            raw_subjects_info = await get_subject_list(arg)
        except ErrorFromServer as e:
            msg = str(e)
        else:
            await ctx.send(embed=make_embed_subject_list(raw_subjects_info, arg))
            return
    await ctx.send(msg)


@bot.command(aliases=["добавить", "addlink"])
async def process_add_link_command(ctx: Context, link=None):
    """Добавляет ссылку на картинку в список ссылок и в файл с ссылаками"""
    if link is None:
        msg = "Необходимо отправить ссылку на картинку"
    else:
        try:
            add_link_to_list_and_file(link)
        except InvalidImageLink as e:
            msg = str(e)
        else:
            msg = "Ссылка успешно добавлена в список"
    await ctx.send(msg)


if __name__ == '__main__':
    init_anime_links_list("anime_pics_links.txt", anime_pics_list)
    bot.run(config.API_TOKEN)
