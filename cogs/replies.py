from discord.ext import commands
import datetime as time

brbMentions = {'ID': 0}


class Replies(commands.Cog):
    """
    When the cog is called, this function runs so this our "setup"
    """
    def __init__(self, bot):
        self.bot=bot
        self.__name__ = "Replies Cog"

    """
    COMMANDS
    """
    @commands.command(name="brb", brief="Be Right Back!", description="Going AFK for a bit? Let Pandora's Box know and I'll remind other users.", aliases=['afk'])
    async def brb(self, ctx, args):
        tdelta = time.timedelta(minutes=(int)(args))
        ctime = time.datetime.today()
        endtime = ctime + tdelta
        await ctx.send(f"Got it! {ctx.author.mention} will be back in {args} minute(s) at: {endtime}")
        brbMentions[ctx.author.id] = endtime

    @commands.command(name="back", brief="Use this when you've returned from being AFK!",
                      description="If you've returned earlier than you anticipated, I'll take note so I don't tell users you're still AFK after you've returned")
    async def back(self, ctx):
        if brbMentions.get(ctx.author.id, 'id not in list') != 'id not in list':
            del brbMentions[ctx.author.id]
            await ctx.send(f"Got it! I've taken note that {ctx.author.mention} has returned.")

    """
    events
    """
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'loaded cog: {self.__name__}')

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author.id != 676930318397079552 and len(ctx.mentions) != 0:
            allMentions = ctx.mentions
            ctime = time.datetime.today()
            for mentions in allMentions:
                if brbMentions.get(mentions.id, 'id not in list') != 'id not in list':
                    backTime = brbMentions.get(mentions.id)
                    if ctime < backTime:
                        await ctx.channel.send(f"Sorry, {ctx.author.mention}, {mentions.name} should be back at {backTime}")


def setup(bot):
    bot.add_cog(Replies(bot))
