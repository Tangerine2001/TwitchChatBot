class Crosser:
    def __init__(self, **kwargs):
        self.userId = kwargs['userId']
        self.username = kwargs['username']
        self.currency = kwargs['currency']
        self.rankName = kwargs['rankName']
        self.hours = kwargs['hours']
        self.firstJoin = kwargs['firstJoin']
        self.lastJoin = kwargs['lastJoin']

    def __eq__(self, other):
        if type(other) == Crosser:
            return self.userId == other.userId
        return False
