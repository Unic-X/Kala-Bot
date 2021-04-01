from discord.ext import commands
import discord as dc
import json,secrets

passw=secrets.token_hex(8)

def write_json(data):
    with open("keys.json",'w') as f:
        json.dump(data, f, indent=4)
with open("keys.json","r") as f:
    data:dict=json.load(f)
    data.update({"BotHash":passw})
    write_json(data)

class OwnerOnly(commands.Cog):
    def __init__(self,bot:commands.Bot):
        self.bot=bot
    @commands.command()
    @commands.is_owner()
    async def bclose(self,ctx,passww):
        if passww==passw:
            try:
                await self.bot.close()
            except:
                pass


