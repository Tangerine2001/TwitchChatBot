from twitchio import User


class Crosser:
    def __init__(self, user: User, **kwargs):
        self.userId = kwargs['user_id']
        self.currency = kwargs['currency']
        self.rankId = kwargs['rank_id']
        self.hours = kwargs['hours']
        self.firstJoin = kwargs['first_join']
        self.lastJoin = kwargs['last_join']

        self.user = user
        self.username = user.name

    def __getattr__(self, func):
        def method(*args):
            try:
                return getattr(self.user, func)(*args)
            except AttributeError as ae:
                print(ae)
                raise AttributeError

        return method

    def __eq__(self, other):
        if type(other) == Crosser:
            return self.userId == other.userId
        return False
