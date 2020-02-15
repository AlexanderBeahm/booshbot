import os
import discord
from config import Config

client = discord.Client()
config = Config()
client_id = config.get_token()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$bb'):
        command_string = message.content.strip().split(" ")
        if '-v' in command_string:
            await message.channel.send('Processing message...')
            await message.channel.send("Split command into %s" % command_string)
        else:
            await message.channel.send('Something just happened.')

client.run(client_id)