from discord.ext import commands
from commands.mod import warning

class errors(commands.Cog):
    global warning
    @commands.Cog.listener()
    async def on_command_error(self,ctx,error):
        if isinstance(error,commands.BotMissingPermissions):
            await ctx.send("I seem to lack some permissions to do dat")
        elif isinstance(error,commands.NoPrivateMessage):
            await ctx.send("This command doesn't work here lmao ded")
        elif isinstance(error,commands.CheckFailure):
            await ctx.send("U miss required permissions")
        elif isinstance(error,commands.MissingPermissions):
            await ctx.send("You lack permission to do this")
        elif isinstance(error,commands.MissingPermissions):
            await ctx.send("Lode lag gye funwaa xDDDD")
        elif isinstance(error,commands.BotMissingPermissions):
            await ctx.send("Lode lag gye funwaa wD")
        elif isinstance(error,commands.CommandOnCooldown):
            if ctx.author.id in warning:
                warning[ctx.author.id]+=1
            else:
                warning[ctx.author.id]=1
            await ctx.send(f"You are sending commands too fast send after {round(error.retry_after,1)}")

def setup(client):
    client.add_cog(errors(client))