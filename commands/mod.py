from discord.ext import commands
import time,datetime,discord as dc

start_time = time.time()

warns={}

class Moderation(commands.Cog):
    @commands.command()
    @commands.cooldown(1, 4)
    async def ban(self, ctx,member:dc.Member=None,*, reason: str=None):
        named_tuple = time.localtime() # get struct_time
        time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
        await ctx.send("Member to ban was Not given!!") if member==None else await member.ban(reason)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx,member:dc.Member=None,*, reason: str=None):
        named_tuple = time.localtime() # get struct_time
        time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
        await ctx.send("Member to ban was Not given!!") if member==None else await member.kick(reason=reason)
    
    @commands.has_permissions(administrator=True)
    @commands.command()
    async def uptime(self, ctx):
            current_time = time.time()
            difference = int(round(current_time - start_time))
            text = str(datetime.timedelta(seconds=difference))
            embed = dc.Embed(colour=0xc8dc6c)
            embed.add_field(name="Uptime", value=text)
            embed.set_footer(text="Dalit-Bot")
            try:
                await ctx.send(embed=embed)
            except dc.HTTPException:
                await ctx.send("Current uptime: " + text)

    @commands.command()
    async def mute(self, ctx,member:dc.Member=None,*, reason: str=None):
        guild=ctx.guild
        muted_role=dc.utils.get(guild.roles,name="General Caste")
        if not muted_role:
            muted_role = await ctx.guild.create_role(name="General Caste")
            await member.add_roles(muted_role,reason=reason)
            await ctx.send(f"Just Reserved a seat {member.mention} for {reason}")
            for channel in guild.channels:
                await channel.set_permissions(muted_role,speak=False,send_messages=False,read_messages=False,read_message_history=False)
        else:
            await member.add_roles(muted_role,reason=reason)
            await ctx.send(f"Just Reserved a seat {member.mention} for {reason}")
    
    @commands.command()
    async def unmute(self, ctx,member:dc.Member=None,*, reason: str=None):
        guild=ctx.guild
        try:
            muted_role=dc.utils.get(guild.roles,name="General Caste")
            await member.remove_roles(muted_role,reason=reason)
            await ctx.send(f"Just UnReserved a seat {member.mention}")
        except:
            await ctx.send(f"Already Chamar {member.mention}")
    @commands.has_permissions(manage_messages=True)
    @commands.command(aliases=['boc', 'bot_c', 'botc', 'botchannel'])
    async def bot_channel(self,ctx,channel:dc.TextChannel=None,role_bot:dc.Role=None):
        if channel==None:
            pass
        elif role_bot==None:
            pass
        else:
            for channel in ctx.guild.channels:
                pass
def setup(bot):
    bot.add_cog(Moderation())

