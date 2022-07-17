import os

from twitchio.ext import commands
from dbconnection import DB
from datetime import datetime


class Bot(commands.Bot):

    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        super().__init__(token=os.environ['TMI_TOKEN'], prefix=os.environ['BOT_PREFIX'], initial_channels=[os.environ['CHANNEL']])
        self.db = DB()

    async def event_ready(self):
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    @commands.command()
    async def hello(self, ctx: commands.Context):
        # Send a hello back!
        await ctx.send(f'Hello {ctx.author.name}!')

    @commands.command()
    async def top(self, ctx: commands.Context):
        # self.db.insert(tableName='users', values=('test3', 100, 'rank1', 0.1, datetime.now(), datetime.now()))
        leaderboardRank = 1
        leaderboardText = ''
        for (user_id, username, currency, rank_name, hours, first_join, last_join) in self.db.getLeaderboard():
            leaderboardText += f'#{leaderboardRank} - [{rank_name}] {username} with {currency} points and {hours} active hours\n'
            leaderboardRank += 1

        await ctx.send(leaderboardText)