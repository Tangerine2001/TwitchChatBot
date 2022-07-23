import os
import re
from datetime import datetime

from twitchio import Message, Channel, User, Chatter
from twitchio.ext import commands
from twitchio.ext.commands import Command

import helper
from dbconnection import DB
from exceptions import GlobalCooldownExceededException
from helper import sample
from variableMappingsHandler import VariableMappingHandler


class TwitchBot(commands.Bot):
    def __init__(self, lilCrossBot):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        super().__init__(token=os.environ['TMI_TOKEN'], prefix=os.environ['BOT_PREFIX'],
                         initial_channels=[os.environ['CHANNEL']])
        self.db = DB()
        self.activeCrossers = []
        self.currentMessage = None
        self.lilCrossBot = lilCrossBot

        self.allRanks = helper.ranks
        self.allCommands = self.lilCrossBot.commands
        self.variableMapper = VariableMappingHandler(self)

        # self.allUsers = self.db.getAllCrossers()

        # Close connection after init. Update db using a Routine
        self.db.close()

    async def event_ready(self):
        # We are logged in and ready to chat and use commands...
        print(f'\nLogged in as | {self.nick}')
        print(f'User id is   | {self.user_id}\n')
        self.lilCrossBot.setChannel(self.get_channel(os.environ['CHANNEL']))

    # async def event_command_error(self, context: commands.Context, error: Exception):
    #     print('##----------------------------------##')
    #     print('#      Command Exception Occurred    #')
    #     print('##----------------------------------##')
    #     print(context.message.content)
    #     print(error)

    async def event_message(self, message: Message) -> None:
        self.currentMessage = message
        if message.author:
            self.lilCrossBot.receivedMessage(message)
            # await self.checkUserIsCrosser(self.connected_channels[0], message.author, message)
        if message.content[0] == '!':
            await self.handle_command(message)

    async def handle_command(self, message: Message):
        cmdString = message.content[1:]

        if len(cmdString) < 1:
            print('Hey bud, why just an exclamation mark?')
            return

        # Define the commands and respective args
        allArgs = cmdString.split()
        cmd = self.allCommands[allArgs[0]]
        args = (message,) + tuple(allArgs[1:]) if len(allArgs) > 1 else (message,)
        print(f'Args: {args}')

        # Cooldown check
        cdCheck = self.db.checkCooldowns(cmd, message)
        if cdCheck is not None:
            if cdCheck is GlobalCooldownExceededException:
                inputStr = sample(helper.exceptions['Global Cooldown Exceptions'])
            else:
                inputStr = sample(helper.exceptions['User Cooldown Exceptions'])
        else:
            inputStr = sample(cmd['Outputs'])
        await message.channel.send(self.variableMapper.getMapping(inputStr, cmd, args))
        # await message.channel.send(helper.replaceVariables(inputStr, cmd, args, self.variableMappings))

    async def event_join(self, channel: Channel, user: Chatter):
        if user.name.lower() == os.environ['BOT_NICKNAME'].lower():
            await channel.send(f'/me has arisen.')
        else:
            await self.checkUserIsCrosser(channel, user)

    async def checkUserIsCrosser(self, channel: Channel, user: Chatter, msg: Message = None):
        joinedUser = await user.user()
        crosser = self.db.getCrosser(joinedUser)

        if not crosser:
            print(f'{joinedUser.display_name} has joined as a first-timer')
            await channel.send(f'Welcome first-timer: {joinedUser.display_name}')
            self.db.insert(tableName='users', values=(joinedUser.id, joinedUser.name, datetime.now()))
            self.activeCrossers.append(self.db.getCrosser(joinedUser))
        elif crosser not in self.activeCrossers:
            print(f'{joinedUser.display_name} has joined!')
            # if user.is_subscriber:
            #     pass
            #     await channel.send(f"Welcome back subscriber: {joinedUser.display_name}. I'm glad to see that you're back!")
            # else:
            #     pass
            #     await channel.send(f"Glad you're back {joinedUser.display_name}!")
            self.db.update(tableName='users', pKeyValue=joinedUser.name)
            self.activeCrossers.append(self.db.getCrosser(joinedUser))
        else:
            pass
            # if msg:
            #     print(f'{joinedUser.display_name}: {msg.content}')

        # joinedUser = Crosser(await user.user())
        # if user.name.lower() == os.environ['BOT_NICKNAME'].lower():
        #     await channel.send(f'/me has arisen.')
        # elif user not in self.allUsers:
        #     await channel.send(f'Welcome first-timer: {user.name}')

    async def event_part(self, user: User):
        if user.name.lower() == os.environ['BOT_NICKNAME'].lower():
            await self.connected_channels[0].send(f'/me is now sleeping. Disturbing him will do nothing')
        else:
            await self.connected_channels[0].send(f"We're another soldier down. {user.name} has left.")

    def getUserName(self, cmd: dict, args: tuple):
        return self.currentMessage.author.name
