from discord.ext.commands import Context
from loguru import logger

logger.add("logs/logs.log", format="{time} {level} {message}", level="INFO")


def command_call_logger_decorator(func):
    async def wrapper(ctx: Context, *args, **kwargs):

        logger.info(
            f"Получено сообщение '{ctx.message.content}' с аргументами [{', '.join(args)}] "
            f"и ключевыми аргументами [{', '.join(kwargs)}] "
            f"(Сервер - {ctx.guild} (id={ctx.guild.id}), "
            f"канал - {ctx.channel} (id={ctx.channel.id}) ) "
            f"Пользователь - {ctx.author.name}, (id={ctx.author.id})")
        return await func(ctx, *args, **kwargs)
    # бот хранит ссылки на корутины, которые вызывает, поэтому если мы все корутины
    # обернем в одну и ту же обертку в этом декораторе,
    # бот будет ссылаться как бы на одну функцию для всех комманд, поэтому вот такие костыли
    wrapper.__name__ = func.__name__
    return wrapper
