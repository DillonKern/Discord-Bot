
#  * Imports
import discord
from discord.ext import commands
import json
import os


# * Bot Initilization and Token Loading
bot = commands.Bot(command_prefix='!') # * we can change this prefix to whatever we want '-' maybe?

with open('config.json', 'r') as fin:
    data = json.load(fin)
    TOKEN = data["token"]

"""
COMMANDS
"""
@bot.command(name="ping", brief="ping the bot!", description="A ping command to Pandora's Box, should respond with 'pong'.")
async def ping(ctx):
    await ctx.send('pong')

@bot.command(name="search", brief="Google search!", description="Don't want to leave the group to google something? Don't worry Pandora's Box got your back.", aliases=['Search', 'Find', 'find'])
async def search(ctx, *, args):

    search_string = "https://www.google.com/search?q="

    for space in args:
        if space == ' ':
            args = args.replace(" ", "+")
    else:
        pass

    link = str(search_string) + str(args)

    embed = discord.Embed(title=f"Search results: {args}", url=link)
    embed.add_field(name="A Google Search turned this up:", value=link)

    await ctx.send(embed=embed)

"""
EVENTS
"""
@bot.event
async def on_ready():
    print(f'Logged in as: {bot.user.name}') 
    print(f'With ID: {bot.user.id}')

@bot.event
async def on_command_error(ctx, error):
    await ctx.send(embed=discord.Embed(title="Something went wrong.", description="Please check the format of your command."))

"""
COG LOADING
"""
@bot.command(hidden=True)
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')


@bot.command(hidden=True)
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')


@bot.command(hidden=True)
async def reload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')
    print(f"{extension} cog, reloaded!")
    await ctx.send(f'{extension} cog, reloaded!')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

"""
No need to touch this.
"""
bot.run(TOKEN)
