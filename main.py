import discord
from discord.ext import commands

import sys
import traceback


TOKEN = "Your token"
BOT_PREFIX = "."

bot = commands.Bot(command_prefix=BOT_PREFIX)


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    return await bot.change_presence(activity=discord.Activity(type=1,
    name="Hosting myself"))


initial_extensions = [
    'cogs.moderation',
    'cogs.data',
    'cogs.welcome',
    'cogs.error',
    'cogs.community',
    'cogs.react',
]


if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f'Failed to load extension {extension}', file=sys.stderr)
            traceback.print_exc()

bot.run(TOKEN)
