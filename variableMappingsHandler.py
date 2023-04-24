import re
from datetime import datetime

import helper


class VariableMappingHandler:
    def __init__(self, twitchChatBot):
        self.tcb = twitchChatBot
        self.tcbDB = self.tcb.db

        self.variableMappings = {
            '${leaderboard}': self.getLeaderboard,
            '${userCooldownDiff}': self.getUserCooldownDiff,
            '${points}': self.getPoints,
            '${userName}': getUserName
        }

    def getMapping(self, inputStr: str, cmd: dict, args: tuple):
        rePattern = '\$\{.*?\}'
        patternMatchesSet = set()
        for patternMatch in re.findall(rePattern, inputStr):
            patternMatchesSet.add(patternMatch)

        if len(patternMatchesSet) > 0:
            for patternMatch in patternMatchesSet:
                inputStr = inputStr.replace(patternMatch, self.variableMappings[patternMatch](cmd, args))
        return inputStr

    def getLeaderboard(self, cmd: dict, args: tuple) -> str:
        try:
            defaultAmount = int(args[1])
        except IndexError or ValueError:
            defaultAmount = 5
        query = f'SELECT * FROM twitch.users ORDER BY currency LIMIT {defaultAmount}'

        cur = self.tcbDB.execute(query)
        ret = cur.fetchall()

        leaderboardRank = 1
        leaderboardText = ''
        for (user_id, username, currency, rank_id, hours, first_join, last_join) in ret:
            leaderboardText += f'#{leaderboardRank} - [{helper.ranks[rank_id]}] {username} with {currency} ' \
                               f'points and {hours} active hours\n'
            leaderboardRank += 1

        return leaderboardText

    def getUserCooldownDiff(self, cmd: dict, args: tuple) -> str:
        commandId = cmd['Command ID']
        userId = args[0].author.id

        query = f"SELECT call_time FROM twitch.called_commands WHERE command_id = {commandId} " \
                f"AND user_id = {userId} ORDER BY call_time DESC"

        cur = self.tcbDB.execute(query)
        ret = cur.fetchall()

        diff = datetime.now().timestamp() - ret[0][0].timestamp()

        return f'{diff: 0.1f}'

    def getPoints(self, cmd: dict, args: tuple) -> str:
        userId = args[0].author.id

        query = f"SELECT currency FROM twitch.users WHERE user_id = {userId}"

        cur = self.tcbDB.execute(query)
        ret = cur.fetchall()

        return str(int(ret[0][0]))


def getUserName(cmd: dict, args: tuple):
    return args[0].author.name
