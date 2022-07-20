import re

iterable = ["${leaderboard}", "Bro, you got somewhere to be? Wait like ${userCooldownDiff} seconds then try again."]


def getLeaderboard(cmd: dict, args: tuple):
    return 'yesLeaderboard'


def getUserCooldownDiff(cmd: dict, args: tuple):
    return 'yesUserCoolDown'


variableMappings = {
        '${leaderboard}': getLeaderboard,
        '${userCooldownDiff}': getUserCooldownDiff
    }


outputStr = []
rePattern = '\$\{.*?\}'
for inputStr in iterable:
    patternMatchesSet = set()
    for patternMatch in re.findall(rePattern, inputStr):
        patternMatchesSet.add(patternMatch)

    if len(patternMatchesSet) > 0:
        for patternMatch in patternMatchesSet:
            inputStr = inputStr.replace(patternMatch, variableMappings[patternMatch]({'cmd': ''}, ('args',)))
    outputStr.append(inputStr)
print(outputStr)