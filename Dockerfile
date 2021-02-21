FROM python:3.9

RUN mkdir -p /usr/src/discord_bot
WORKDIR /usr/src/discord_bot

COPY . /usr/src/discord_bot

RUN pip install --no-cache-dir -r requirements.txt
ENTRYPOINT "python bot.py"
