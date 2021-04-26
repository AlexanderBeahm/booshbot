from igdb_api import covers_get, games_search, genres_get, platforms_get
import discord
import logging
import os
import requests
import time

from igdb.wrapper import IGDBWrapper
from discord import Embed

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
    
    # if message.content.startswith('$hello'):
    #     await message.channel.send('Hello!')
    # if message.content.startswith('$shutdown'):
    #     await message.channel.send('Shutting down...')
    #     await client.close()
    if message.content.startswith('$g'):
        '''With a wrapper instance already created'''
        refresh_token(os.environ['TWITCH_CLIENT_ID'], os.environ['TWITCH_CLIENT_SECRET'])

        request = str.split(message.content,'$g')[1].strip()
        game_json_object = games_search(igdb_wrapper, request)
        if game_json_object is None:
            embedVar = discord.Embed(title="Game Result", description="{} searched for '{}'".format(message.author, request), color=0xFF0000)
            embedVar.add_field(name="Error", value="No results found.", inline=False)
            await message.channel.send(embed=embedVar)
        else:
            game_cover = "//www.pngrepo.com/download/236434/game-controller-gamepad.png"
            genres = None
            platforms = None
            if "cover" in game_json_object and game_json_object["cover"] is not None:
                game_cover = covers_get(igdb_wrapper, game_json_object["cover"])[0]["url"]

            if "genres" in game_json_object and game_json_object["genres"] is not None:
                genres = genres_get(igdb_wrapper, game_json_object["genres"])

            if "platforms" in game_json_object and game_json_object["platforms"] is not None:
                platforms = platforms_get(igdb_wrapper, game_json_object["platforms"])

            #format genres into a (hyperlink)[url] pattern seprated by commas
            formatted_genres = None
            formatted_platforms = None
            if genres is not None:
                formatted_genres = format_hyperlinks(genres)
            if platforms is not None:
                formatted_platforms = format_hyperlinks(platforms)

            formatted_name = format_hyperlinks([game_json_object])

            embedVar = discord.Embed(title="Game Result", description="{} searched for '{}'".format(message.author, request), color=0x00ff00)
            embedVar.add_field(name="Title", value=formatted_name, inline=False)
            embedVar.add_field(name="Summary", value=game_json_object["summary"], inline=False)
            if formatted_platforms is not None:
                embedVar.add_field(name="Platforms", value=formatted_platforms, inline=False)
            if formatted_genres is not None:
                embedVar.add_field(name="Genres", value=formatted_genres, inline=False)
            embedVar.set_thumbnail(url="https:{}".format(game_cover))
            await message.channel.send(embed=embedVar)

    
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

def format_hyperlinks(links):
    formatted_links = []
    for link in links:
        formatted_links.append(str.format('[{}]({})', link["name"], link["url"]))
    return ', '.join([str(formatted_link) for formatted_link in formatted_links])

def main():
    logger.info(f"Token is: {os.environ['DISCORD_BOT_TOKEN']}")
    refresh_token(os.environ['TWITCH_CLIENT_ID'], os.environ['TWITCH_CLIENT_SECRET'])
    client.run(os.environ['DISCORD_BOT_TOKEN'])

logger.info("Starting up BooshBot...")
main()
logger.info("Shutting down BooshBot...")