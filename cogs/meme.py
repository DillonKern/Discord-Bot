from discord.ext import commands
import discord
import requests
import json
#import giphy_client
#from giphy_client.rest import ApiException
import aiohttp
import random
import urllib


class Meme(commands.Cog):
    
    def __init__(self, bot):
        self.bot=bot
        self.__name__ = "Meme Cog"
       
    @commands.command(name="meme", brief="serve up a gif")
    async def giphy(self, ctx, search=None):

        session = aiohttp.ClientSession()
        if search is None:
            response = await session.get('http://api.giphy.com/v1/gifs/random?api_key=geEyH0RfvDuMSTGE9mfc3lEONqhwMOYe')
            await session.close()
            data = await response.json()
            gif = data['data']['images']['original']['url']
            embed = discord.Embed(title="", description="")
            embed.set_image(url=gif)
            await ctx.send(embed=embed)
        else:
            search.replace(' ', '+')
            response = await session.get('http://api.giphy.com/v1/gifs/search?q=' + search + '&api_key=geEyH0RfvDuMSTGE9mfc3lEONqhwMOYe&limit=10')
            await session.close()
            data = await response.json()
            gif_choice = random.randint(0, 9)
            gif = data['data'][gif_choice]['images']['original']['url']
            embed = discord.Embed(title="", description="")
            embed.set_image(url=gif)
            await ctx.send(embed=embed)
            await session.close()



    @commands.Cog.listener()
    async def on_ready(self):
        print(f'loaded cog: {self.__name__}')


def setup(bot):
    bot.add_cog(Meme(bot))
