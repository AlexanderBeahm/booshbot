import discord
import logging
import os
import requests
import time

from igdb.wrapper import IGDBWrapper
from igdb.igdbapi_pb2 import GameResult

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
client = discord.Client()
igdb_wrapper = None
next_twitch_refresh = 0.0
twitch_token = ''

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
    if message.content.startswith('$gamers'):
        '''With a wrapper instance already created'''
        refresh_token(os.environ['TWITCH_CLIENT_ID'], os.environ['TWITCH_CLIENT_SECRET'])
        # JSON API request
        byte_array = igdb_wrapper.api_request(
            'games',
            'fields id, name; offset 0; where platforms=48;'
          )
        # parse into JSON however you like...

        # Protobuf API request
        byte_array = igdb_wrapper.api_request(
            'games.pb', # Note the '.pb' suffix at the endpoint
            'fields id, name; offset 0; where platforms=48;'
          )
        games_message = GameResult()
        games_message.ParseFromString(byte_array) # Fills the protobuf message object with the response
        await message.channel.send(games_message)

    
def refresh_token(client_id, client_secret):
    global next_twitch_refresh
    global igdb_wrapper
    if(next_twitch_refresh - 10000 <= time.process_time()):
        refresh_url = "https://id.twitch.tv/oauth2/token"
        response = requests.post(url= refresh_url, params={'client_id':client_id, 'client_secret':client_secret, 'grant_type':'client_credentials'})
        refreshToken = response.json()
        access_token = refreshToken['access_token']
        expires_in = refreshToken['expires_in']
        next_twitch_refresh = time.process_time() + expires_in
        twitch_token = access_token
        igdb_wrapper = IGDBWrapper(client_id, twitch_token)

def main():
    logger.info(f"Token is: {os.environ['DISCORD_BOT_TOKEN']}")
    refresh_token(os.environ['TWITCH_CLIENT_ID'], os.environ['TWITCH_CLIENT_SECRET'])
    client.run(os.environ['DISCORD_BOT_TOKEN'])

logger.info("Starting up BooshBot...")
main()
logger.info("Shutting down BooshBot...")