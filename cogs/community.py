import aiohttp
import discord
from discord.ext import commands
import urllib.parse, urllib.request, re
import wikipedia
import asyncio
import random
import re


dedicate_cat_api_key = "Your api key "
global cat_counter


class ComCog(commands.Cog, name='Community'):

    def __init__(self, bot):
        self.bot = bot

    # youtube search
    @commands.command()
    async def youtube(self, ctx, *, search):
        """⛩ Search up something on youtube """
        query_string = urllib.parse.urlencode({
            'search_query': search
        })
        htm_content = urllib.request.urlopen(
            'http://www.youtube.com/results?' + query_string
        )
        search_results = re.findall('href=\"\\/watch\\?v=(.{11})', htm_content.read().decode())
        await ctx.send('http://www.youtube.com/watch?v=' + search_results[0])

    @commands.command()
    async def server(self, ctx):
        """⛩ Check info about current server """
        if ctx.invoked_subcommand is None:
            findbots = sum(1 for member in ctx.guild.members if member.bot)

            embed = discord.Embed()

            if ctx.guild.icon:
                embed.set_thumbnail(url=ctx.guild.icon_url)
            if ctx.guild.banner:
                embed.set_image(url=ctx.guild.banner_url_as(format="png"))

            embed.add_field(name="Server Name", value=ctx.guild.name, inline=True)
            embed.add_field(name="Server ID", value=ctx.guild.id, inline=True)
            embed.add_field(name="Members", value=ctx.guild.member_count, inline=True)
            embed.add_field(name="Bots", value=findbots, inline=True)
            embed.add_field(name="Owner", value=ctx.guild.owner, inline=True)
            embed.add_field(name="Region", value=ctx.guild.region, inline=True)
            await ctx.send(content=f"ℹ information about **{ctx.guild.name}**", embed=embed)

    @commands.command(aliases=['wikipedia'])
    async def wiki(self, ctx, *, query):
        '''⛩ Search up something on wikipedia '''
        em = discord.Embed(title=str(query))
        em.set_footer(text='Powered by wikipedia.org')
        try:
            result = wikipedia.summary(query)
            if len(result) > 2000:
                em.description = f"Result is too long. View the website [here](https://wikipedia.org/wiki/{query.replace(' ', '_')}), or just google the subject."
                return await ctx.send(embed=em)
            em.description = result
            await ctx.send(embed=em)
        except wikipedia.exceptions.DisambiguationError as e:
            options = '\n'.join(e.options)
            em.description = f"**Options:**\n\n{options}"
            await ctx.send(embed=em)
        except wikipedia.exceptions.PageError:
            em.description = 'Error: Page not found.'
            await ctx.send(embed=em)

    @commands.command()
    async def suggest(self, ctx, *, idea: str):
        """⛩ Suggest something! """
        suggest = self.bot.get_channel(659890046110793768)
        embed = discord.Embed(title="💡 💡 💡", colour=0x95efcc, description=f"{idea}")
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/avatars/627103119116861450/a0e9221a3f9298d727fd53db6ad307ac.jpg?size=1024")
        embed.set_author(name=f'  {ctx.message.author.name} has a great idea ')
        await suggest.send(embed=embed)
        await ctx.send("Your idea has been successfully sent to the channel. Thank you!", delete_after=3)

    @commands.command()
    async def advertise_mods(self, ctx, *, advertise: str):
        """ ⛩Advertise mods for commons problem """
        mods_channel = self.bot.get_channel(637204637857873930)
        embed = discord.Embed(title=f'from {ctx.message.author.name}', description=advertise)
        await mods_channel.send(embed=embed)
        await ctx.send("Mods has been advertised", delete_after=3)

    @commands.command()
    async def flip(self, ctx):
        '''⛩ Flip a coin! '''
        msg = await ctx.send('Flipping...')
        await asyncio.sleep(4)
        await msg.edit(content=random.choice(('Heads!', 'Tails!')))

    @commands.command()
    async def test(self, ctx, *args):
        """⛩ test command"""
        await ctx.send('{} arguments: {}'.format(len(args), ', '.join(args)))

    @commands.command()
    async def random_cat(self, ctx: commands.Context):
        """Random cat picture"""
        async with aiohttp.ClientSession() as session:
            async with session.get("http://aws.random.cat/meow") as r:
                if r.status == 200:
                    js = await r.json()
                    em = discord.Embed(title="Random Cat!",
                                       colour=discord.Colour.dark_green())
                    em.set_image(url=js["file"])
                    em.set_footer(text="Cats, cats and cats",
                                  icon_url=f"https://cdn.discordapp.com/avatars/{self.bot.user.id}/{self.bot.user.avatar}.png?size=64")
                    await ctx.send(embed=em)
                else:
                    em = discord.Embed(title="Error",
                                       description="Couldn't reach random.cat.\nTry again later.",
                                       colour=discord.Colour.red())
                    await ctx.send(embed=em)

    @commands.command()
    async def test(self, ctx, *args):
        await ctx.send('{} arguments: {}'.format(len(args), ', '.join(args)))

    class Slapper(commands.Converter):
        async def convert(self, ctx, argument):
            to_slap = random.choice(ctx.guild.members)
            return '{0.author} slapped {1} because *{2}*'.format(ctx, to_slap, argument)

    @commands.command()
    async def slap(self, ctx, *, reason: Slapper):
        await ctx.send(reason)


def setup(bot):
    bot.add_cog(ComCog(bot))
    print('Community is loaded')
