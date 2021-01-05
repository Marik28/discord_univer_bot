from pprint import pprint

from discord.ext import commands
from discord.ext.commands import Context

import config
from exceptions import ErrorFromServer
from services import get_week_parity, get_day_schedule, make_beautiful_day_view, get_week_schedule, test_embed_features, \
    make_embed_day_schedule

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print('Бот подключился к серверу')


@bot.command(name='hello')
async def hello(ctx: Context):
    await ctx.send('Дарова, чел')


@bot.command(name='расписание')
async def process_day_schedule_command(ctx: Context, day: str, parity=None):
    if parity is None:
        parity = get_week_parity()
    try:
        row_day_schedule = get_day_schedule(day, parity)
    except ErrorFromServer as e:
        await ctx.send(str(e))
        return
    await ctx.send(embed=make_embed_day_schedule(row_day_schedule, parity))


@bot.command(name='неделя')
async def process_week_schedule_command(ctx: Context, parity=None):
    if parity is None:
        parity = get_week_parity()
    get_week_schedule(parity)


@bot.command(name='test')
async def process_test_command(ctx: Context):
    await ctx.send(embed=test_embed_features())

bot.run(config.API_TOKEN)
