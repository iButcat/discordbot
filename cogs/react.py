import discord
from discord.ext import commands
import sqlite3
import re

class ReactCog(commands.Cog, name='Reactions'):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, reaction):
        main = sqlite3.connect('main.db')
        cursor = main.cursor()
        if '<:' in str(reaction.emoji):
            cursor.execute(f"SELECT emoji, role, message_id, channel_id FROM reaction WHERE guild_id = '{reaction.guild_id}' and message_id = '{reaction.message_id}' and emoji = '{reaction.emoji.id}'")
            result = cursor.fetchone()
            guild = self.bot.get_guild(reaction.guild_id)
            if result is None:
                return
            elif str(reaction.emoji.id) in str(result[0]):
                on = discord.utils.get(guild.roles, id=int(result[1]))
                user = guild.get_member(reaction.user_id)
                await user.add_roles(on)
            else:
                return
        elif '<:' not in str(reaction.emoji):
            cursor.execute(f"SELECT emoji, role, message_id, channel_id FROM reaction WHERE guild_id = '{reaction.guild_id}' and message_id = '{reaction.message_id}' and emoji = '{reaction.emoji}'")
            result = cursor.fetchone()
            guild = self.bot.get_guild(reaction.guild_id)
            if result is None:
                return
            elif result is not None:
                on = discord.utils.get(guild.roles, id=int(result[1]))
                user = guild.get_member(reaction.user_id)
                await user.add_roles(on)
            else:
                return

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, reaction):
        main = sqlite3.connect('main.db')
        cursor = main.cursor()
        if '<:' in str(reaction.emoji):
            cursor.execute(f"SELECT emoji, role, message_id, channel_id FROM reaction WHERE guild_id ='{reaction.guild_id}' and message_id = '{reaction.message_id}' and emoji = '{reaction.emoji.id}' ")
            result = cursor.fetchone()
            guild = self.bot.get_guild(reaction.guild_id)
            if result is None:
                return
            elif str(reaction.emoji.id) in str(result[0]):
                on = discord.utils.get(guild.roles, id=int(result[1]))
                user = guild.get_member(reaction.user_id)
                await user.remove_roles(on)
            else:
                return
        elif '<:' not in str(reaction.emoji):
            cursor.execute(f"SELECT emoji, role, message_id, channel_id FROM reaction WHERE guild_id ='{reaction.guild_id}' and message_id = '{reaction.message_id}' and emoji = '{reaction.emoji.id}' ")
            result = cursor.fetchone()
            guild = self.bot.get_guild(reaction.guild_id)
            if result is None:
                return
            elif result is not None:
                on = discord.utils.get(guild.roles, id=int(result[1]))
                user = guild.get_member(reaction.user_id)
                await user.remove_roles(on)
            else:
                return

    @commands.command()
    async def roleadd(self, ctx, channel: discord.TextChannel, messageid, emoji, role: discord.Role):
        main = sqlite3.connect('main.db')
        cursor = main.cursor()
        cursor.execute(f"SELECT emoji, role, message_id, channel_id FROM reaction WHERE guild_id = '{ctx.message.guild.id}' and message_id = '{messageid}'")
        result = cursor.fetchone()
        if '<:' in emoji:
            emm = re.sub(':.*?:','',emoji).strip('<>')
            if result is None:
                sql = ('INSERT INTO reaction(emoji, role, message_id, channel_id, guild_id) VALUES(?,?,?,?,?)')
                val = (emm, role.id, messageid, channel.id, ctx.guild.id)
                msg = await channel.fetch_message(messageid)
                em = self.bot.get_emoji(int(emm))
                await msg.add_reaction(em)
            elif str(messageid) not in str(result[3]):
                sql = ('INSERT INTO reaction(emoji, role, message_id, channel_id, guild_id) VALUES(?,?,?,?,?)')
                val = (emm, role.id, messageid, channel.id, ctx.guild.id)
                msg = await channel.fetch_message(messageid)
                em = self.bot.get_emoji(int(emm))
                await msg.add_reaction(em)
        elif '<:' not in emoji:
            if result is None:
                sql = ('INSERT INTO reaction(emoji, role, message_id, channel_id, guild_id) VALUES(?,?,?,?,?)')
                val = (emoji, role.id, messageid, channel.id, ctx.guild.id)
                msg = await channel.fetch_message(messageid)
                await msg.add_reaction(emoji)
            elif str(messageid) not in str(result[3]):
                sql = ('INSERT INTO reaction(emoji, role, message_id, channel_id, guild_id) VALUES(?,?,?,?,?)')
                val = (emoji, role.id, messageid, channel.id, ctx.guild.id)
                msg = await channel.fetch_message(messageid)
                await msg.add_reaction(emoji)
        cursor.execute(sql, val)
        main.commit()
        cursor.close()
        main.close()

    @commands.command()
    async def roleremove(self, ctx, messageid=None, emoji=None):
        main = sqlite3.connect('main.db')
        cursor = main.cursor()
        cursor.execute(f"SELECT emoji, role, message_id, channel_id FROM reaction WHERE guild_id = '{ctx.guild.id}' and message_id = '{messageid}'")
        result = cursor.fetchone()
        if '<:' in emoji:
            emm = re.sub(':.*?;', '', emoji).strip('<>')
            if result is None:
                await ctx.send('That reaction was not found on that message.')
            elif str(messageid) in str(result[2]):
                cursor.execute(f"DELETE FROM reaction WHERE guild_id = '{ctx.guild.id}' and message_id = '{messageid}' and emoji = '{emm}' ")
                await ctx.send('Reaction has been removed')
            else:
                await ctx.send('That reaction was not found on that message')
        elif '<:' not in emoji:
            if result is None:
                await ctx.send('That reaction was not found on that message.')
            elif str(messageid) in str(result[2]):
                cursor.execute(
                    f"DELETE FROM reaction WHERE guild_id = '{ctx.guild.id}' and message_id = '{messageid}' and emoji = '{emoji}' ")
                await ctx.send('Reaction has been removed')
            else:
                await ctx.send('That reaction was not found on that message')
        main.commit()
        cursor.close()
        main.close()


def setup(bot):
    bot.add_cog(ReactCog(bot))
    print('React is loaded')

