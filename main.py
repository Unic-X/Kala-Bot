import discord as dc
from discord.ext import commands
import utils

'''
To do:
1. Remainder setter
2. Avoiding data losses ie. before closing the bot by using database🛑
3.Fandom/Wiki scraper (using API for speed and reliablity)🛑
4.Moderator Functions like
    1.Ban/Mute/Kick/Warn  ✅
    2. Logging the actions by the user in a db or a (json file)not preffered as the storage will be heavy
5.Tembanning/Blocking the user for spamming the commands🛑🛑🛑🛑
6.Anime info from MAL ✅
7.Uptime ✅
8. Adding custom prefix to each server as per need🛑 

'''

intents=dc.Intents.default()
intents.members=True
intents.presences=True

cogs=(
    "commands.anime",
    "commands.mod"
)
if __name__=="__main__":
    client=commands.Bot(command_prefix="!",intents=intents)
    for cog in cogs:
        client.load_extension(cog)
    client.run(utils.get_key_from_json("token"))