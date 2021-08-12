from discord.ext import commands
import discord as dc
import aiohttp,math,random
from commands.utils import *


url = "https://api.alquran.cloud/"

arguments={
    "language",
    "page",
}

class Quran(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
    def assign_endpoints(self,string):
        args = to_dict(string)
        for arg in args.keys():
            check=arg.lower()
            if check == "ayah":
                return url+f"/ayah/{args[arg]}"
            else:
                return None
    @commands.group(name="quran",invoke_without_command=True)
    @commands.cooldown(1, 4)
    async def quran(self,ctx,*,argstr):
        a=self.assign_endpoints(argstr)
        if a ==None:
            await ctx.send("Wrong parameters")
        else:
            async with aiohttp.ClientSession() as session:
                response = await fetch(session,a)
                await ctx.send(response["data"]["text"])
    @quran.command(name="random")
    async def random(self,ctx):
        try:
            async with aiohttp.ClientSession() as session:
                    response = await fetch(session,url+f"/ayah/{random.randint(1,6236)}")
                    await ctx.send(response["data"]["text"])
        except Exception as e:
            print(e)
    @quran.command(name="oftheday")
    async def aotd(self,ctx):
        pass



def setup(bot):
    bot.add_cog(Quran(bot))

