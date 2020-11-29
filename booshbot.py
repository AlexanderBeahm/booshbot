import discord
import logging
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
client = discord.Client()

@client.event
async def on_ready():
    logger.info('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

def main():
    logger.info(f"Token is: {os.environ['DISCORD_BOT_TOKEN']}")
    client.run(os.environ['DISCORD_BOT_TOKEN'])

logger.info("Starting up BooshBot...")
main()
logger.info("Shutting down BooshBot...")