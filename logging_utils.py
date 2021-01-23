# from discord.ext.commands import Context
# from loguru import logger
#
# logger.add("logs/logs.log", format="{time} {level} {message}", level="INFO", rotation="1 MB", compression="zip")
#
#
# def command_call_logger_decorator(func):
#     async def wrapper(ctx: Context, *args, **kwargs):
#         raw_command = ctx.message.content.split(" ")[0]
#         logger.info(
#             f"Вызвана корутина {func.__name__}. "
#             f"Получено сообщение '{raw_command}' с аргументами [{', '.join(args)}] "
#             f"и ключевыми аргументами [{', '.join(kwargs)}] "
#             f"(Сервер - {ctx.guild} (id={ctx.guild.id}), "
#             f"канал - {ctx.channel} (id={ctx.channel.id}) ) "
#             f"Пользователь - {ctx.author.name}, (id={ctx.author.id})")
#         return await func(ctx, *args, **kwargs)
#     # бот хранит ссылки на корутины, которые вызывает, поэтому если мы все корутины
#     # обернем в одну и ту же обертку в этом декораторе,
#     # бот будет ссылаться как бы на одну функцию для всех комманд, поэтому вот такие костыли
#     wrapper.__name__ = func.__name__
#     return wrapper
