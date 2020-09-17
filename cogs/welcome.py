import discord
from discord.ext import commands
import datetime
import sqlite3


class WelcomeCog(commands.Cog, name='Welcome'):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT channel_id FROM main WHERE guild_id = {member.guild.id}")
        result = cursor.fetchone()
        if result is None:
            return
        else:
            cursor.execute(f"SELECT msg FROM main WHERE guild_id = {member.guild.id}")
            result1 = cursor.fetchone()
            members = len(list(member.guild.members))
            mention = member.mention
            user = member.name
            guild = member.guild
            embed = discord.Embed(colour=0x95efcc, description=str(result1[0]).format(members=members, mention=mention, user=user, guild=guild))
            embed.set_thumbnail(url=f"{member.avatar_url}")
            embed.set_author(name=f"{member.name}", url=f"{member.avatar_url}")
            embed.set_footer(text=f"{member.guild}", icon_url=f"{member.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()

            channel = self.bot.get_channel(id=int(result[0]))

            await channel.send(embed=embed)

    @commands.group(invoke_whitout_command=True)
    async def welcome(self, ctx):
        await ctx.send('Available commands : \nwelcome channel <#channel>\nwelcome text <message>')

    @welcome.command()
    async def channel(self, ctx, channel: discord.TextChannel):
        if ctx.message.author.guild_permissions.manage_messages:
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT channel_id FROM main WHERE guild_id = {ctx.guild.id}")
            result = cursor.fetchone()
            if result is None:
                sql = ("INSERT INTO main(guild_id, channel_id) VALUES(?,?) ")
                val = (ctx.guild.id, channel.id)
                await ctx.send(f"Channel has been set to {channel.mention}")
            elif result is None:
                sql = ("UPDATE main SET channel_id = ? WHERE guild_id = ?")
                val = (channel.id, ctx.guild.id)
                await ctx.send(f"Channel has been set to {channel.mention}")
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()

    @welcome.command()
    async def text(self, ctx, *, text):
        if ctx.message.author.guild_permissions.manage_messages:
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT msg FROM main WHERE guild_id = {ctx.guild.id}")
            result = cursor.fetchone()
            if result is None:
                sql = ("INSERT INTO main(guild_id, msg) VALUES(?,?) ")
                val = (text, ctx.guild.id)
                await ctx.send(f"Messages has been set ’{text}’")
            elif result is None:
                sql = ("UPDATE main SET msg = ? WHERE guild_id = ?")
                val = (text, ctx.guild.id)
                await ctx.send(f"Message has been update to ’{text}’")
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()

def setup(bot):
    bot.add_cog(WelcomeCog(bot))
    print('welcome is ready')
