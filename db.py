import os
from datetime import datetime

import mysql.connector

import helper
from helper import sample
from twitchio import User, Message
from twitchio.ext.commands import Context

from crosser import Crosser
from exceptions import GlobalCooldownExceededException, UserCooldownExceededException


class DB:
    def __init__(self):
        # Connect to db and create cursor
        self.conn = mysql.connector.connect(
            host=os.environ['DB_HOST'],
            user=os.environ['DB_USERNAME'],
            password=os.environ['DB_PASSWORD']
        )
        self.cur = self.conn.cursor()

    def insert(self, tableName: str, values: tuple):
        if tableName == 'users':
            # Values should get passed in as userId, username, first_join
            defaultValues = (values[0], values[1], 0, 1, 0, values[2], values[2])
            query = f'INSERT INTO twitch.users (user_id, username, currency, rank_id, hours, first_join, last_join) ' \
                    f'VALUES (%s, %s, %s, %s, %s, %s, %s)'
        elif tableName == 'called_commands':
            # Values should get passed in as commandId, userId, call_time, command args info
            defaultValues = (values[0], values[1], values[2], str(values[3]))
            query = f'INSERT INTO twitch.called_commands (command_id, user_id, call_time, command_info) ' \
                    f'VALUES (%s, %s, %s, %s)'
        else:
            defaultValues = ()
            query = f'INSERT INTO twitch.{tableName} (username, currency, rank_name, hours, first_join, last_join) VALUES (%s, %s, %s, %s, %s, %s)'
        self.cur.execute(query, defaultValues)
        self.commit()

    def update(self, tableName: str, pKeyValue):
        if tableName == 'users':
            # Values should get passed in as userId, username, first_join
            defaultValues = (datetime.now(), pKeyValue)
            query = f'UPDATE twitch.users SET last_join = %s WHERE username = %s'
        else:
            defaultValues = ()
            query = f'INSERT INTO twitch.{tableName} (username, currency, rank_id, hours, first_join, last_join) VALUES (%s, %s, %s, %s, %s, %s)'
        self.cur.execute(query, defaultValues)
        self.commit()

    def checkCooldowns(self, cmd: dict, msg: Message):
        commandId = cmd['Command ID']
        globalCD = cmd['Global Cooldown']
        userCD = cmd['User Cooldown']
        userId = msg.author.id

        query = f"SELECT call_time FROM twitch.called_commands WHERE command_id = {commandId} " \
                f"ORDER BY call_time DESC"
        self.cur.execute(query)
        ret = self.cur.fetchall()
        diff = datetime.now().timestamp() - ret[0][0].timestamp()
        if len(ret) > 0 and diff < globalCD:
            return GlobalCooldownExceededException()

        query = f"SELECT call_time FROM twitch.called_commands WHERE command_id = {commandId} " \
                f"AND user_id = {userId} ORDER BY call_time DESC"
        self.cur.execute(query)
        ret = self.cur.fetchall()
        diff = datetime.now().timestamp() - ret[0][0].timestamp()
        if len(ret) > 0 and diff < userCD:
            return UserCooldownExceededException()

        self.insert(tableName='called_commands', values=(commandId, userId,
                                                         datetime.now(), msg.content))

    def getCrosser(self, user: User):
        query = f"SELECT * FROM twitch.users WHERE username = '{user.name}'"
        self.cur.execute(query)

        ret = self.cur.fetchall()
        if len(ret) < 1:
            return None
        else:
            columns = [col[0] for col in self.cur.description]
            ret = Crosser(user, **dict(zip(columns, ret[0])))
            return ret

    def execute(self, query, values=None):
        if values:
            self.cur.execute(query, values)
        else:
            self.cur.execute(query)
        return self.cur

    def connect(self):
        self.conn.connect()

    def commit(self):
        self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()
