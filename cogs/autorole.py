import discord
from discord.ext import commands


class AutoRole(commands.Cog):
    def __init__(self, bot):
        self.bot=bot
        self.__name__="AutoRole Cog"


    @commands.Cog.listener()
    async def on_ready(self):
        print(f'loaded cog: {self.__name__}')

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):

        channel = member.guild.system_channel

        if channel is not None:

            try:
                name = member.display_name
                default_role = member.guild.get_role(704795177650225172)

                # * Personal Message to the User
                embed = discord.Embed(title=f"One More Thing!",
                                    description="You've automatically been given the 'Class Member' role! Check it out by selecting the group menu in the top-right!")

                await channel.send(embed=embed)
            except Exception as e:
                print(f"Something went wrong sending the welcome message to {name}\nError: {e}")

        try:
            await member.add_roles(default_role, reason="New member, default role assignment")
            print(f"Default Role: Attendee - Successfully added to {member} ")
        except Exception:
            print("Something went wrong adding role!")

def setup(bot):
    bot.add_cog(AutoRole(bot))