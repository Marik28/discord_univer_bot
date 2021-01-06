from discord.ext import commands
from discord.ext.commands import Context

import config
from api_helpers import get_teacher_list, get_day_schedule, get_week_schedule
from exceptions import ErrorFromServer, EmptyJson
from services import get_week_parity, make_embed_day_schedule, make_embed_week_schedule, COMMAND_PREFIX, \
    make_help_embed_message, make_embed_teacher_list

bot = commands.Bot(command_prefix=COMMAND_PREFIX)


@bot.event
async def on_ready():
    print('Бот подключился к серверу')


@bot.command(name='hello')
async def hello(ctx: Context):
    await ctx.send('Дарова, чел')


@bot.command(name='расписание')
async def process_day_schedule_command(ctx: Context, day: str, parity=None):
    """Узнает расписание на конкретный день недели. Если не указана четность недели, берется четность текущей недели"""
    if parity is None:
        parity = get_week_parity()
    try:
        raw_day_schedule = get_day_schedule(day, parity)
    except ErrorFromServer as e:
        await ctx.send(str(e))
        return
    except EmptyJson:
        await ctx.send(f"В этот день ({day}|{parity}) нет пар")
    else:
        await ctx.send(embed=make_embed_day_schedule(raw_day_schedule, parity))


@bot.command(name='неделя')
async def process_week_schedule_command(ctx: Context, parity=None):
    """Узнает расписание на целую неделю. Если не указана четность недели, берется четность текущей недели"""
    if parity is None:
        parity = get_week_parity()
    try:
        raw_week_schedule = get_week_schedule(parity)
    except ErrorFromServer as e:
        await ctx.send(str(e))
        return
    else:
        await ctx.send(embed=make_embed_week_schedule(raw_week_schedule, parity))


@bot.command(name='info')
async def process_test_command(ctx: Context):
    """Обрабатывает команду 'info'. Отправляет Embed со списком команд и примерами их использования"""
    await ctx.send(embed=make_help_embed_message())


@bot.command(aliases=['препод', 'преподы'])
async def process_teacher_command(ctx: Context, arg=None):
    """Обрабатывает команду 'препод'"""
    try:
        raw_teachers_info = get_teacher_list(arg)
    except ErrorFromServer as e:
        await ctx.send(str(e))
        return
    else:
        await ctx.send(embed=make_embed_teacher_list(raw_teachers_info))


if __name__ == '__main__':
    bot.run(config.API_TOKEN)
