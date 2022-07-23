import re

import helper


class VariableMappingHandler:
    def __init__(self, twitchChatBot):
        self.tcb = twitchChatBot
        # self.tcbDB = self.tcb.db

        self.variableMappings = {
            '${leaderboard}': self.getLeaderboard,
            '${userCooldownDiff}': self.getLeaderboard,
            '${points}': self.getLeaderboard,
            '${userName}': self.getLeaderboard
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

    def getLeaderboard(self, cmd: str, args: tuple) -> str:
        try:
            defaultAmount = int(args[1])
        except IndexError or ValueError:
            defaultAmount = 5
        query = f'SELECT * FROM twitch.users ORDER BY currency LIMIT {defaultAmount}'

        # cur = self.tcbDB.execute(query)
        # ret = cur.fetchall()
        ret = [(1, 2, 3, 4, 5, 6, 7)]

        leaderboardRank = 1
        leaderboardText = ''
        for (user_id, username, currency, rank_id, hours, first_join, last_join) in ret:
            leaderboardText += f'#{leaderboardRank} - [{helper.ranks[rank_id]}] {username} with {currency} ' \
                               f'points and {hours} active hours\n'
            leaderboardRank += 1

        return leaderboardText
