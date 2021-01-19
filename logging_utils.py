from typing import Callable

from discord.ext.commands import Context
from loguru import logger


def command_call_logger_decorator(func):
    async def wrapper(ctx: Context, *args, **kwargs):
        logger.info(
            f"Получено сообщение '{ctx.message.content}' с аргументами [{', '.join(args)}] "
            f"и ключевыми аргументами [{', '.join(kwargs)}] "
            f"(Сервер - {ctx.guild} (id={ctx.guild.id}), "
            f"канал - {ctx.channel} (id={ctx.channel.id}) ) "
            f"Пользователь - {ctx.author.name}, (id={ctx.author.id})")
        return await func(ctx, *args, **kwargs)

    return wrapper


logger.add("logs/logs.log", format="{time} {level} {message}", level="INFO")
