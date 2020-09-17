import discord
from discord.ext import commands


class ModCog(commands.Cog, name='Moderation'):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def purge(self, ctx, *, number: int = None):
        """ ⛩ Purge messages """
        if ctx.author.guild_permissions.manage_messages:
            try:
                if number is None:
                    await ctx.send("You must input a number!!")
                else:
                    deleted = await ctx.message.channel.purge(limit=number)
                    await ctx.send(f'Messages purged by {ctx.message.author.mention}: {len(deleted)}', delete_after=3.0)
            except:
                await ctx.send("I can't purge messages here", delete_after=3.0)
        else:
            await ctx.send("You don't have the permission to this command", delete_after=3.0)

    @commands.command()
    async def kick(self, ctx, user: discord.Member, *, reason=None):
        """ ⛩ Kick someone """
        if user.guild_permissions.manage_messages:
            await ctx.send("I can't kick this user because they are mods or admins", delete_after=3.0)
        elif ctx.message.author.guild_permissions.kick_members:
            if reason is None:
                await ctx.guild.kick(user=user, reason='None')
                await ctx.send(f'{user} has been kicked.')
            else:
                await ctx.guild.kick(user=user, reason=reason)
                await ctx.send(f'{user} has been kicked.')
        else:
            await ctx.send('You do not have the permissions for this command', delete_after=3.0)

    @kick.error
    async def kick_error(self, ctx, error):
        await ctx.send('There has been an error in the kick command')

    @commands.command()
    async def ban(self, ctx, user: discord.Member, *, reason=None):
        """ ⛩ Ban someone """
        if user.guild_permissions.manage_messages:
            await ctx.send("I can't kick this user because they are mods or admins")
        elif ctx.message.author.guild_permissions.ban_members:
            if reason is None:
                await ctx.guild.ban(user=user, reason='None')
                await ctx.send(f'{user} has been kicked.')
            else:
                await ctx.guild.ban(user=user, reason=reason)
                await ctx.send(f'{user} has been kicked.')
        else:
            await ctx.send('You do not have the permissions for this command', delete_after=5.0)

    @commands.command(name="avatar")
    async def avatar(self, ctx, *, member: discord.Member = None):
        """ ⛩ Show your pfp with different format """
        if not member:
            member = ctx.author

        embed = discord.Embed(
            colour=discord.Color.gold(),
            title=f"{member.name}'s Avatar",
            description=f"[PNG]({member.avatar_url_as(size=1024, format='png')}) | "
                        f"[JPEG]({member.avatar_url_as(size=1024, format='jpeg')}) | "
                        f"[WEBP]({member.avatar_url_as(size=1024, format='webp')})"
        )
        embed.set_author(icon_url=ctx.author.avatar_url_as(format="png"), name=ctx.author.name)

        if member.is_avatar_animated():
            embed.description += f" | [GIF]({member.avatar_url_as(size=1024, format='gif')})"
            embed.set_image(url=f"{member.avatar_url_as(size=1024, format='gif')}")
        else:
            embed.set_image(url=f"{member.avatar_url_as(size=1024, format='png')}")

        return await ctx.send(embed=embed)

    @commands.command()
    @discord.ext.commands.has_role(636897705960013830)
    async def dm(self, ctx, user: discord.Member, title: str, *, msg: str):
        """⛩ Dm someone (only mods) """
        embed = discord.Embed(title=f"{title}", colour=0x95efcc, description=f"{msg}")
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/avatars/627103119116861450/a0e9221a3f9298d727fd53db6ad307ac.jpg?size=1024")
        embed.set_author(name="⛩Great old time⛩",
                         icon_url="https://cdn.discordapp.com/avatars/627103119116861450/a0e9221a3f9298d727fd53db6ad307ac.jpg?size=1024")
        embed.set_footer(text=" 🎊 Mods 🎊 ")
        try:
            await user.send(embed=embed)
            await ctx.message.delete()
            await ctx.send("Success! Your DM has been sent!")
        except discord.ext.commands.MissingPermissions:
            await ctx.send("You could get away with DM people without permissions.")
        except:
            await ctx.send("Error")

    @commands.command()
    @discord.ext.commands.has_role(636897705960013830)
    async def bans(self, ctx):
        """⛩ Show all the banned users """
        try:
            bans = await ctx.guild.bans()
        except:
            return await ctx.send("You don't have the permission to see bans list :)")
        em = discord.Embed(title=f'List of banned Members ({len(bans)}):')
        em.description = ', '.join({str(b.user) for b in bans})
        await ctx.send(embed=em)

    # suppose to be sending event message
    @commands.command()
    @discord.ext.commands.has_role(636897705960013830)
    async def announce(self, ctx, channel: discord.TextChannel, title: str, *, msg: str):
        """⛩ Announce something (mods only) """
        embed = discord.Embed(title=f"{title}", colour=0x95efcc, description=f"{msg}")
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/avatars/627103119116861450/a0e9221a3f9298d727fd53db6ad307ac.jpg?size=1024")
        embed.set_author(name="⛩Announcement⛩",
                         icon_url="https://cdn.discordapp.com/avatars/627103119116861450/a0e9221a3f9298d727fd53db6ad307ac.jpg?size=1024")
        embed.set_footer(text=" 🎊 Mods 🎊 ")
        try:
            await channel.send(embed=embed)
            await ctx.message.delete()
            await ctx.send("Successfuly send message to the channel")
        except discord.ext.commands.MissingPermissions:
            await ctx.send('no permission')
        except:
            await ctx.send('Error')

    @commands.Cog.listener()
    @discord.ext.commands.has_role(684745206104457237)
    async def role_ban(self, ctx):
        if discord.Member.has_role(684745206104457237):
            await ctx.channel.send('the statement works')
        else:
            print('error')


def setup(bot):
    bot.add_cog(ModCog(bot))
    print('Moderation is loaded')
