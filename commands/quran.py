from discord.ext import commands
import discord as dc
import aiohttp,math,random
from commands.utils import *
import shlex,inspect,re

url = "https://api.alquran.cloud/"

arguments={
    "language",
    "page",

}

class Quran(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
    def assign_endpoints(self,string):
        args = dict(e.split("=") for e in re.split('; |, |\*|\s|\n',string))
        for arg in args.keys():
            check=arg.lower()
            if check == "ayah":
                return url+f"/ayah/{args[arg]}"
            elif check=="random":
                ayah=random.randint(1,6236)
                return url+f"/ayah/{ayah}"
            else:
                return None

    @commands.command()
    @commands.cooldown(1, 4)
    async def quran(self,ctx,*,argstr):
        a=self.assign_endpoints(argstr)
        if a ==None:
            await ctx.send("Wrong parameters")
        else:
            async with aiohttp.ClientSession() as session:
                response = await fetch(session,a)
                await ctx.send(response["data"]["text"])


def setup(bot):
    bot.add_cog(Quran(bot))