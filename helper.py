#
# def getOrDefault(dictToGet: dict, key: str, defaultValue):
#     if key not in dictToGet.keys() or dictToGet[key] is None:
#         return defaultValue
#     return dictToGet[key]
#
#
# def convertUsersToCrosser(users: list[dict]) -> list[Crosser]:
#     crossers = []
#     # (user_id, username, currency, rank_name, hours, first_join, last_join)
#     for user in users:
#         crossers.append(Crosser(**{
#             "userId": getOrDefault(user, "userId", -1),
#             "username": getOrDefault(user, "username", 'None'),
#             "currency": getOrDefault(user, "currency", 0),
#             "rankName": getOrDefault(user, "rankName", 'None'),
#             "hours": getOrDefault(user, "hours", 0),
#             "firstJoin": getOrDefault(user, "firstJoin", datetime.now()),
#             "lastJoin": getOrDefault(user, "lastJoin", datetime.now())
#         }))
#
#     return crossers
import json
import random
import re

ranks = {
    1: 'Crosser',
    2: 'Jogger',
    3: 'Runner',
    4: 'Sprinter'
}

commands = json.load(open('Json/commands.json'))
exceptions = json.load(open('Json/cooldownExceptions.json'))


def sample(iterable):
    return iterable[random.randint(0, len(iterable) - 1)]


def replaceVariables(inputStr: str, cmd: dict, args: tuple, variablesMappings: dict) -> str:
    rePattern = '\$\{.*?\}'
    patternMatchesSet = set()
    for patternMatch in re.findall(rePattern, inputStr):
        patternMatchesSet.add(patternMatch)

    if len(patternMatchesSet) > 0:
        for patternMatch in patternMatchesSet:
            inputStr = inputStr.replace(patternMatch, variablesMappings[patternMatch](cmd, args))
    return inputStr
