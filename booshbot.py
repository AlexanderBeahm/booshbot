from igdb_api import covers_get_by_id, games_search, genres_get, platforms_get, release_dates_get
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
filtered_users = os.environ['FILTERED_BOOSHBOT_USERS'].split(',')

@client.event
async def on_ready():
    logger.info('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message :discord.Message):

    if message.author == client.user:
        return

    # F
    if message.content.startswith('$finalmessage') and is_filtered_user(message.author.name):
        await message.channel.send("https://www.youtube.com/watch?v=DPEvF8l9LDM")

    # G
    if message.content.startswith('$giantsteps') and is_filtered_user(message.author.name):     
        await message.channel.send("https://www.youtube.com/watch?v=30FTr6G53VU&ab_channel=Jazzman2696")
    elif message.content.startswith('$g ') and is_filtered_user(message.author.name):
        '''With a wrapper instance already created'''
        refresh_token(os.environ['TWITCH_CLIENT_ID'], os.environ['TWITCH_CLIENT_SECRET'])

        request = str.split(message.content,'$g')[1].strip()
        escaped_request = request.translate(str.maketrans({"-":  r"\-",
                                          "]":  r"\]",
                                          "\\": r"\\",
                                          "^":  r"\^",
                                          "$":  r"\$",
                                          "*":  r"\*",
                                          ".":  r"\."}))
        game_json_object = games_search(igdb_wrapper, escaped_request)
        if game_json_object is None:
            embedVar = discord.Embed(title="Game Result", description="{} searched for '{}'".format(message.author, request), color=0xFF0000)
            embedVar.add_field(name="Error", value="No results found.", inline=False)
            await message.channel.send(embed=embedVar)
        else:
            game_cover = "//www.pngrepo.com/download/236434/game-controller-gamepad.png"
            genres = None
            platforms = None
            release_date='????'
            summary = ''
            if "cover" in game_json_object and game_json_object["cover"] is not None:
                game_cover = covers_get_by_id(igdb_wrapper, game_json_object["cover"])[0]["url"]

            if "genres" in game_json_object and game_json_object["genres"] is not None:
                genres = genres_get(igdb_wrapper, game_json_object["genres"])

            if "platforms" in game_json_object and game_json_object["platforms"] is not None:
                platforms = platforms_get(igdb_wrapper, game_json_object["platforms"])

            if "release_dates" in game_json_object and game_json_object["release_dates"] is not None:
                release_date_result = release_dates_get(igdb_wrapper, [game_json_object["release_dates"][0]])[0]
                if "y" in release_date_result: 
                    release_date = release_date_result["y"]
            
            if "summary" in game_json_object and game_json_object["summary"] is not None:
                summary = game_json_object["summary"]
                

            #format genres into a (hyperlink)[url] pattern seprated by commas
            formatted_genres = ''
            formatted_platforms = ''
            formatted_summary = ''
            if genres is not None:
                formatted_genres = format_hyperlinks(genres)
            if platforms is not None:
                formatted_platforms = format_hyperlinks(platforms)
            if summary is not None and len(summary) >= 1024:
                formatted_summary = summary[0:1019]
                formatted_summary = formatted_summary + "..."
            else:
                formatted_summary = summary


            formatted_name = format_hyperlinks([game_json_object])

            #create the embed
            embedVar = discord.Embed(description="**{} ({})** *{}*".format(formatted_name,release_date,formatted_platforms), color=0x00ff00)
            #embedVar.add_field(name="Title", value=formatted_name, inline=False)
            if formatted_summary is not None and formatted_summary != '':
                embedVar.add_field(name="Summary", value='> {}'.format(formatted_summary), inline=False)
            if formatted_genres is not None and formatted_genres != '':
                embedVar.add_field(name="Genres", value=formatted_genres, inline=False)
            embedVar.set_thumbnail(url="https:{}".format(game_cover))
            await message.channel.send(embed=embedVar)

        # H
        if message.content.startswith('$h') and is_filtered_user(message.author.name):
            await message.channel.send("**Available Commands**\n\n$g *<Game Name>*\n> Search for game in IGDB (ex: `$g Among Us`)")


    
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

def is_filtered_user(name):
    return len(filtered_users) == 0 or '*' in filtered_users or name in filtered_users

def main():
    logger.info(f"Token is: {os.environ['DISCORD_BOT_TOKEN']}")
    refresh_token(os.environ['TWITCH_CLIENT_ID'], os.environ['TWITCH_CLIENT_SECRET'])
    client.run(os.environ['DISCORD_BOT_TOKEN'])

logger.info("Starting up BooshBot...")
main()
logger.info("Shutting down BooshBot...")