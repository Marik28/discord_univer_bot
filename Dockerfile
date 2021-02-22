FROM python:3.9

RUN mkdir -p /usr/src/discord_bot
WORKDIR /usr/src/discord_bot
COPY . .
RUN mkdir -p logs
RUN pip install --no-cache-dir -r requirements.txt
RUN ls

RUN chmod a+x ./run.sh
ENTRYPOINT ["./run.sh"]
