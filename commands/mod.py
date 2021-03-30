from discord.ext import commands
import time,datetime,discord as dc

start_time = time.time()

class Moderation(commands.Cog):
    @commands.command()
    @commands.cooldown(1, 4)
    async def ban(self, ctx,member:dc.Member=None,*, reason=None):
        named_tuple = time.localtime() # get struct_time
        time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
        await ctx.send("Member to ban was Not given!!") if member==None else await member.ban(reason=reason)

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
    
    @commands.command()
    async def ui(self,ctx,*,member:dc.Member=None):

        if member==None:
            member=ctx.author
        if member.mobile_status == dc.Status.online:
            mobile_sts="Mobile status <:online1:778941955740663828>"
        elif member.mobile_status == dc.Status.idle: 
            mobile_sts="Mobile status <:idle1:778942115136143370>"
        elif member.mobile_status == dc.Status.dnd:
            mobile_sts="Mobile status <:dnd:778942294233186374>"
        elif member.mobile_status == dc.Status.offline or member.mobile_status == dc.Status.invisible:
            mobile_sts="Mobile status <:ded1:778942365527703562>"

        if member.web_status == dc.Status.online:
           web_sts="Web status <:online1:778941955740663828>"
        elif member.web_status == dc.Status.idle:
            web_sts="Web status <:idle1:778942115136143370>"
        elif member.web_status == dc.Status.dnd:
            web_sts="Web status <:dnd:778942294233186374>"
        elif member.web_status == dc.Status.offline or member.web_status == dc.Status.invisible:
            web_sts="Web status <:ded1:778942365527703562>"

        if member.desktop_status == dc.Status.online:
            desk_sts="Desktop status <:online1:778941955740663828>"
        elif member.desktop_status == dc.Status.idle:
            desk_sts="Desktop status <:idle1:778942115136143370>"
        elif member.desktop_status == dc.Status.dnd:
            desk_sts="Desktop status <:dnd:778942294233186374>"
        elif member.desktop_status == dc.Status.offline or member.desktop_status == dc.Status.invisible:
            desk_sts="Desktop status <:ded1:778942365527703562>"

        is_bot="<a:cross1:779006336854786058>"

        if member.bot == True:
            is_bot="<a:right:779006338671968256>"
        else:
            is_bot="<a:cross1:779006336854786058>"
        roles=[]
        for i in member.roles:
            roles.append(i.mention)
        e=dc.Embed()
        e.add_field(name=f"About {member}",value=f"<:arrow:778989582620426260> **Nick Name :** {member.display_name} \n <:arrow:778989582620426260> **User ID : ** {member.id} \n <:arrow:778989582620426260> **Joined Server ** {member.joined_at.strftime('%d-%b-%Y')} \n <:arrow:778989582620426260> **Joined Discord : ** {member.created_at.strftime('%d-%b-%Y')} \n <:arrow:778989582620426260> **Bot :** {is_bot} \n <:arrow:778989582620426260> **Avatar URL :** [Click here]({member.avatar_url})",inline=False)
        e.add_field(name="Status",value='{} | <:phone:778984480772980796> Mobile Status \n {} | <:web:778984466470797342> Web Status \n {} | <:pc:778984512372998204> Desktop Status'.format(mobile_sts,web_sts,desk_sts),inline=True)
        e.set_thumbnail(url=member.avatar_url)
        if len(member.roles)==1:
            e.add_field(name=f"Roles({len(member.roles)-1})",value="None")
        else:
            e.add_field(name=f"Roles({len(member.roles)-1})",value="\n".join(roles[1:]))

        await ctx.send(content=f"<:info:779039384296882217> Information about **{member.name}**",embed=e)
def setup(bot):
    bot.add_cog(Moderation())

