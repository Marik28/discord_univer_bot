FROM python:3.9

WORKDIR /usr/src/discord_bot

COPY requirements.txt ./
RUN python3 -m venv venv
RUN source venv/bin/activate
RUN pip install --no-cahce-dir -r requirements.txt

