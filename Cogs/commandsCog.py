from datetime import datetime

from twitchio.ext import commands
from twitchio.ext.commands import Cog, Context

from customCommand import CustomCommand


class CommandsCog(Cog):
    def __init__(self, bot):
        self.bot = bot
        # self.bot.add_command(CustomCommand('top', 'Get top', 0, 5, 0, self.top))
        # self.bot.add_command(CustomCommand('hello', 'Say hello!', 0, 0, 0, self.hello))
        self.success = True

    async def cog_check(self, ctx: Context) -> bool:
        # Run before the start of every command
        cmd = ctx.command.name
        ret = self.bot.db.checkCooldown(self.bot, cmd, ctx)
        if ret is None:
            self.success = True
        else:
            self.success = False
            await ctx.channel.send(str(ret))
        return self.success

    @commands.command()
    async def hello(self, ctx: Context):
        # Send a hello back!
        await ctx.send(f"Hello {ctx.author.name[:-1]}! Welcome to {ctx.channel.name}' stream. "
                       f"Settle in and enjoy yourself B)")

    @commands.command()
    async def top(self, ctx: Context, *args):
        if len(args) > 0:
            try:
                defaultAmount = int(args[0])
            except ValueError:
                defaultAmount = 5
                await ctx.channel.send(f"My brother in crossing you're supposed to put a number after !top. "
                                       f"{args[0]} is not a number!")
        else:
            defaultAmount = 5

        leaderboardRank = 1
        leaderboardText = ''
        for (user_id, username, currency, rank_id, hours, first_join, last_join) in self.bot.db.getLeaderboard(
                defaultAmount):
            leaderboardText += f'#{leaderboardRank} - [{self.bot.ranks[rank_id]}] {username} with {currency} points and {hours} active hours\n'
            leaderboardRank += 1
        await ctx.channel.send(leaderboardText)

    async def cog_error(self, exception: Exception) -> None:
        print('-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-')
        pass

    async def cog_command_error(self, ctx: Context, exception: Exception) -> None:
        print('##########################')
        pass
