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
    @commands.Cog.listener()
    async def on_ready(self):
        for owner_id in self.bot.owner_ids:
            try:
                to_dm = self.bot.get_user(owner_id)
                await to_dm.send(passw)
            except Exception as e:
                pass
    def __init__(self,bot:commands.Bot):
        self.bot=bot
    @commands.command()
    @commands.is_owner()
    @commands.dm_only()
    async def bclose(self,ctx,passww):
        if passww==passw:
            try:
                await self.bot.close()
            except:
                pass
    @bclose.error
    async def bclose_error(self,ctx,error):
        if isinstance(error, commands.PrivateMessageOnly):
            await ctx.send(f'''{ctx.author.mention}, You cannot use this command in the server \n
        this command is DM only''',delete_after=5.0)


def setup(bot):
    bot.add_cog(OwnerOnly(bot))