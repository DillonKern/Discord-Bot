import discord
from discord.ext import commands


class Admin_Area(commands.Cog):
    def __init__(self, bot):
        self.bot=bot
        self.__name__ = "Admin Area Cog"

    """
    COMMANDS
    """
    # * At a later date we should probably add permissions or 'hidden=True' to this command
    @commands.command(name="clear", aliases=['purge'], brief="Remove messages [Admin Only]", description="Messages are annoying, if you're an Admin, use this to get rid of those pesky messages!")
    async def clear(self, ctx, amount=2):
        if amount <= 0:
            await ctx.send("I can't purge 0 messages. Try again!")

        await ctx.channel.purge(limit=amount)

    """
    EVENTS
    """
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'loaded cog: {self.__name__}')


def setup(bot):
    bot.add_cog(Admin_Area(bot))