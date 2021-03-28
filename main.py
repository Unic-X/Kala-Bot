import discord as dc
from discord.ext import commands
from commands import utils
import secrets,json

intents=dc.Intents.default()
intents.members=True
intents.presences=True

client=commands.Bot(command_prefix="!",intents=intents)

passw=secrets.token_hex(8)

def write_json(data):
    with open("keys.json",'w') as f:
        json.dump(data, f, indent=4)

with open("keys.json","r") as f:
    data:dict=json.load(f)
    data.update({"BotHash":passw})
    write_json(data)

'''
To do:
1. Remainder setter
2. Avoiding data losses ie. before closing the bot by using database🛑
3.Fandom/Wiki scraper (using API for speed and reliablity) 🚧 WIP 🚧
4.Moderator Functions like
    1.Ban/Mute/Kick/Warn  ✅
    2. Logging the actions by the user in a db or a (json file)not preffered as the storage will be heavy
5.Tembanning/Blocking the user for spamming the commands🛑🛑🛑🛑
6.Anime info from MAL ✅
7.Uptime ✅
8. Adding custom prefix to each server as per need🛑 

'''
@commands.is_owner()
@client.command()
async def bclose(ctx,passww):
    if passww==passw:
        try:
            await client.close()
        except:
            pass

cogs=(
    "commands.anime",
    "commands.mod",
    "commands.server",
    "commands.Fandom.dark_souls"
)
if __name__=="__main__":
    for cog in cogs:
        client.load_extension(cog)
    client.run(utils.get_key_from_json("token"))