import discord
import logging
import os
import feedparser

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
client = discord.Client()

rym_rss = "https://rateyourmusic.com/~The_Booshnaw/data/rss"

def parserss(feed):
    formattedstring = '**Recent Activity:'
    for item in feed["items"]:
        itemstring = f'\n{item["title"]}\t{item["link"]}'
        if len(formattedstring + itemstring) > 2000:
            break
        formattedstring = formattedstring + itemstring

    return formattedstring

@client.event
async def on_ready():
    logger.info('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    if message.content.startswith('$shutdown'):
        await message.channel.send('Shutting down...')
        await client.close()
    if message.content.startswith('$recent'):
        feed = feedparser.parse(rym_rss)
        feed_message = parserss(feed)
        await message.channel.send(feed_message)

def main():
    logger.info(f"Token is: {os.environ['DISCORD_BOT_TOKEN']}")
    client.run(os.environ['DISCORD_BOT_TOKEN'])

logger.info("Starting up BooshBot...")
main()
logger.info("Shutting down BooshBot...")