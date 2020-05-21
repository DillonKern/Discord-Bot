import json
import os
from datetime import datetime
import discord
from discord.ext import commands


class MLB(commands.Cog):

    def __init__(self, bot):
        self.__name__ = "MLB Schedule"
        self.bot = bot
        self.schedule = []
        self.today = datetime.now().date()

    def load_mlb_schedule(self):
        with open(os.path.join(os.path.dirname(__file__), 'assets/mlb_schedule.json')) as infile:
            data = json.load(infile)
        for game in data:
            self.schedule.append(game)

    # listener
    @commands.Cog.listener()
    async def on_ready(self):
        self.load_mlb_schedule()
        print(f'loaded cog: {self.__name__}')

    # command
    @commands.command(aliases=['mlb'], brief="See The MLB Schedule for today")
    async def get_schedule(self, ctx):
        today_str = self.today.strftime("%B %-d, %Y")
        today_compare = self.today.strftime("%Y-%m-%d")
        current_games = []

        for games in self.schedule:
            if games['date'] == today_compare:
                current_games.append(games)
        embed = discord.Embed(title=f"MLB Games for {today_str}")

        count = 1
        for game in current_games:
            embed.add_field(name=f"Game {count}",
                            value=f"{game['visitor_name']} vs {game['home_name']} @ {game['gametimeET']} ET")
            count += 1

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(MLB(bot))
