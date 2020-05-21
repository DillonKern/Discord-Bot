import json
import os
from datetime import datetime as dt
from datetime import timedelta

import discord
from darksky import forecast
from discord.ext import commands
from uszipcode import SearchEngine


class Weather(commands.Cog):
    def __init__(self, bot):
        self.bot=bot
        self.__name__="Weather Cog"
        self.key = ""
        self.search = SearchEngine(simple_zipcode=True, db_file_dir=os.path.join(os.path.dirname(__file__), 'assets/'))

        self.setup()

    """
    COMMANDS
    """
    @commands.command(name="weather", brief="Find the weather by Zipcode!", description="Give a Zipcode argument to recieve the weekly weather summary in that area!")
    async def weather(self,ctx, arg):
        # TODO: Provide an error case if a command that requires an argument is not given one.
        try:
            # * Turn the user input into an integer
            user_zipcode = str(arg)

            if len(user_zipcode) != 5:
                raise ValueError("The zipcode is not the correct length")

            user_zipcode = int(user_zipcode)

            # * Use the zipcode database to retrieve geographical data from the zipcod - returns None on error.
            zipcode_info = self.search.by_zipcode(user_zipcode)
            zipcode_info.to_dict()

            # * On success, retrieve a valid latitude and longitude
            latitude = zipcode_info.lat
            longitude = zipcode_info.lng

        
            # * try to get the forecast from a lat and long, return a Discord Error Embed on error.
            location = forecast(self.key, latitude, longitude)

            # * Retrieve today's date from datetime and parse only the date.
            today = dt.now().date()

            # * Initialize an embed from the zipcode data providing a base title and description.
            embed = discord.Embed(title=f"Weather for {zipcode_info.city}, {zipcode_info.state_long}", description=f"Zipcode: {arg}")

            # * Add to the embed a field for the 7 days following today's date.
            for day in location.daily.data:
                embed.add_field(name=f"{today.strftime('%A - %x')}",value=f"{day.summary}\nHigh: {day.apparentTemperatureHigh}\nLow: {day.apparentTemperatureLow}")
                today = today + timedelta(days=1)

        # * On Error send a seperate Embed
        except Exception as e:
            await ctx.send(embed=discord.Embed(title="Something Went Wrong - Error Description Below", description=f"{e}"))

        # * On success of the try/catch send the inital long embed from the for loop
        await ctx.send(embed=embed)

        # * Reset today's date to today and send a second summary embed.
        today = dt.now().date()
        await ctx.send(embed=discord.Embed(title=f"Week Summary for {today}",description=f"{location.daily.summary}"))

    """
    EVENTS
    """
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'loaded cog: {self.__name__}')

    """
    HELPERS
    """
    def setup(self):
        # * Open the config file and get the API Key
        with open(os.path.join(os.path.dirname(__file__), 'assets/config.cfg'), "r") as config:
            data = json.load(config)
            self.key = data["API_KEY"]


def setup(bot):
    bot.add_cog(Weather(bot))
