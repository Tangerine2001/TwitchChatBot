from datetime import datetime
from crosser import Crosser


def getOrDefault(dictToGet: dict, key: str, defaultValue):
    if key not in dictToGet.keys() or dictToGet[key] is None:
        return defaultValue
    return dictToGet[key]


def convertUsersToCrosser(users: list[dict]) -> list[Crosser]:
    crossers = []
    # (user_id, username, currency, rank_name, hours, first_join, last_join)
    for user in users:
        crossers.append(Crosser(**{
            "userId": getOrDefault(user, "userId", -1),
            "username": getOrDefault(user, "username", 'None'),
            "currency": getOrDefault(user, "currency", 0),
            "rankName": getOrDefault(user, "rankName", 'None'),
            "hours": getOrDefault(user, "hours", 0),
            "firstJoin": getOrDefault(user, "firstJoin", datetime.now()),
            "lastJoin": getOrDefault(user, "lastJoin", datetime.now())
        }))

    return crossers
