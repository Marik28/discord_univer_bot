FROM python:3.9

RUN mkdir -p /usr/src/discord_bot
WORKDIR /usr/src/discord_bot
COPY . .
RUN mkdir -p logs
RUN pip install --no-cache-dir -r requirements.txt

#RUN chmod +x write_data.py
RUN chmod +x run.sh


#ENV BASE_API_URL=http://marik28.pythonanywhere.com/api/v1/
#ENV DISCORD_BOT_API_TOKEN=NzgwNzQyMDEzODc1NzgxNjY0.X7zgqQ.Tcf2XPzOlNT0ujQPbUgW1Wb7gvE
#ENV ANIME_LINKS_DB=0
#ENV ANIME_LINKS_SET=anime_links
#ENV COMMAND_PREFIX=.

#RUN python write_data.py
CMD ["sh", "run.sh"]