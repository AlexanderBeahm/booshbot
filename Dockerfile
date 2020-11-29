FROM python:3

ARG discord_bot_token

WORKDIR /user/src/app
ENV DISCORD_BOT_TOKEN=$discord_bot_token

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./booshbot.py" ]