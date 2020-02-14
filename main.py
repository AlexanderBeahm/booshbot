import os
import discord

client = discord.Client()

client_id = "MzkxNzQ4MzE4NTUzODMzNDgy.XjWq4w.lw9O9zntDPkkBudq-fC04AdhjAw        "

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run(client_id)