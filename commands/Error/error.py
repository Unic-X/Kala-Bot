from discord.ext import commands

class errors(commands.Cog):

    @commands.Cog.listener()
    async def on_command_error(self,ctx,error):
        if isinstance(error,commands.BotMissingPermissions):
            print(1)
            await ctx.send("I seem to lack some permissions to do dat")
        elif isinstance(error,commands.NoPrivateMessage):
            print(2)
            await ctx.send("This command doesn't work here lmao ded")
        elif isinstance(error,commands.CheckFailure):
            await ctx.send("U miss required permissions")
        elif isinstance(error,commands.MissingPermissions):
            await ctx.send("You lack permission to do this")
        elif isinstance(error,commands.MissingPermissions):
            await ctx.send("Lode lag gye funwaa xDDDD")
        elif isinstance(error,commands.BotMissingPermissions):
            await ctx.send("Lode lag gye funwaa wD")
        elif isinstance(error,commands.CommandInvokeError):
            await ctx.send("idk")

def setup(client):
    client.add_cog(errors(client))