import discord
from discord.ext import commands


class Greeting(commands.Cog):
    """
    When the cog is called, this function runs so this our "setup"
    """
    def __init__(self, bot):
        self.bot=bot
        self.__name__ = "Greeting Cog"


    """
    COMMANDS
    """
    @commands.command(name="hello", aliases=['hi', 'hey'], brief="Say hi to the bot!", description="Say hello to Pandora's Box, and the box will respond with your name!")
    async def hello(self, ctx):
        await ctx.send(f"Hi There {ctx.author.mention}")

    """
    EVENTS
    """
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'loaded cog: {self.__name__}')

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):

        channel = member.guild.system_channel

        if channel is not None:

            try:
                name = member

                # * Personal Message to the User
                embed = discord.Embed(title=f"Welcome {name.display_name}!",
                                    description=f"Greetings {name.mention}!\nWelcome to the Server! I am Pandora's Box\nType '!help' to see what I can do!")

                await channel.send(embed=embed)
            except Exception as e: # * Catch ANY error and save it into the variable e
                print(
                    f"Something went wrong sending the welcome message to {name}\nError: {e}")

#  * Cog setup and latching onto our main pandora.py file
def setup(bot):
    bot.add_cog(Greeting(bot))