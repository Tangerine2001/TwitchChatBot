from collections import Callable
from twitchio.ext import commands


class CustomCommand(commands.Command):
    def __init__(self, commandInput: str, description: str, globalCD: int, userCD: int, permissionRank: str, func: Callable, **attrs):
        self.description = description
        self.globalCD = globalCD
        self.userCD = userCD
        self.permissionRank = permissionRank
        super().__init__(commandInput, func, **attrs)
