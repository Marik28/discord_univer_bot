from discord.ext import commands
from discord.ext.commands import Context

from api_helpers import get_teacher_list, get_day_schedule, get_week_schedule, get_subject_list
import config
from datetime_helpers import from_word_to_day, DAY_SPECIAL_WORDS, get_week_parity
from embed_handlers import make_embed_image
from exceptions import ErrorFromServer, InvalidImageLink
# from logging_utils import logger, command_call_logger_decorator
# from redis_utils.redis_api import add_link_to_redis
from redis_utils.redis_api import get_redis_connection, LinksSetManager
from services import make_embed_day_schedule, make_embed_week_schedule, make_help_embed_message, \
    make_embed_teacher_list, make_embed_subject_list, init_anime_links_list, add_link_to_list_and_file, \
    make_brief_subject_list

bot = commands.Bot(command_prefix=config.COMMAND_PREFIX)


@bot.event
async def on_ready():
    print("Бот подключился к серверу")
    # logger.info("Бот подключился к серверу")


@bot.command(aliases=['расписание', 'пары'])
# @command_call_logger_decorator
async def process_day_schedule_command(ctx: Context, day: str = None, parity: str = None):
    """Узнает расписание на конкретный день недели. Если не указана четность недели, берется четность текущей недели.
    Результат отправляет в виде Embed-сообщения"""
    if day is None:
        msg = f"Нужно указать хотя бы день недели, на который узнает расписание.{config.ERROR_MSG_BIT}"
    else:
        if day in DAY_SPECIAL_WORDS:
            day = from_word_to_day[day]()
        if parity is None:
            parity = get_week_parity()
        try:
            raw_day_schedule = await get_day_schedule(day, parity)
        except ErrorFromServer as e:
            msg = str(e)
        else:
            await ctx.send(embed=make_embed_day_schedule(raw_day_schedule, day, parity))
            return
    await ctx.send(msg)


@bot.command(name='неделя')
# @command_call_logger_decorator
async def process_week_schedule_command(ctx: Context, parity: str = None):
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
# @command_call_logger_decorator
async def process_test_command(ctx: Context):
    """Отправляет Embed-сообщение со списком команд и их описанием"""
    await ctx.send(embed=make_help_embed_message())


@bot.command(aliases=['препод', 'преподы', 'преподаватель', 'преподаватели'])
# @command_call_logger_decorator
async def process_teacher_command(ctx: Context, arg=None):
    """Производит поиск по преподам на совпадение Ф./И./О. препода.
    Возвращает список совпадений в виде Embed-сообщения"""
    if arg is None:
        msg = f"Небходимо написать имя/фамилию/отчество препода. {config.ERROR_MSG_BIT}"
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
# @command_call_logger_decorator
async def process_subjects_command(ctx: Context, arg=None):
    """Производит поиск по предметам на совпадение части названия.
    Возвращает список совпадений в виде Embed-сообщения"""
    try:
        raw_subjects_info = await get_subject_list(arg)
    except ErrorFromServer as e:
        msg = str(e)
    else:
        if arg is not None:
            reply_msg = make_embed_subject_list(raw_subjects_info, arg)
        else:
            reply_msg = make_brief_subject_list(raw_subjects_info)
        await ctx.send(embed=reply_msg)
        return
    await ctx.send(msg)


@bot.command(aliases=["добавить", "addlink"])
# @command_call_logger_decorator
async def process_add_link_command(ctx: Context, link=None):
    """Добавляет ссылку на картинку в список ссылок и в файл с ссылаками"""
    if link is None:
        msg = "Необходимо отправить ссылку на картинку"
    else:
        try:
            # msg = add_link_to_redis(link)
            msg = add_link_to_list_and_file(link)
        except InvalidImageLink as e:
            msg = str(e)
    await ctx.send(msg)


@bot.command(aliases=["картинка", "аниме"])
# @command_call_logger_decorator
async def process_get_image_command(ctx: Context):
    """Отправляет рандомную пикчу из бд"""
    msg = make_embed_image()
    await ctx.send(embed=msg)


# @logger.catch()
def main():
    # logger.info("Начинаю подключение к серверу ...")

    # init_anime_links_list("anime_pics_links.txt", config.anime_pics_list)
    bot.run(config.API_TOKEN)


if __name__ == '__main__':
    main()
