import os
import mysql.connector

from helper import convertUsersToCrosser

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
            query = f'INSERT INTO twitch.users (username, currency, rank_name, hours, first_join, last_join) VALUES (%s, %s, %s, %s, %s, %s)'
        else:
            query = f'INSERT INTO twitch.{tableName} (username, currency, rank_name, hours, first_join, last_join) VALUES (%s, %s, %s, %s, %s, %s)'
        self.connect()
        self.cur.execute(query, values)
        self.close()

    def getLeaderboard(self):
        query = f'SELECT * FROM twitch.users ORDER BY currency LIMIT 5'

        self.connect()
        self.cur.execute(query)
        ret = self.cur.fetchall()

        self.close()
        return ret

    def getAllCrossers(self):
        query = f'SELECT * FROM twitch.users'

        self.connect()
        self.cur.execute(query)
        columns = [col[0] for col in self.cur.description]
        ret = convertUsersToCrosser([dict(zip(columns, row)) for row in self.cur.fetchall()])

        self.close()
        return ret

    def connect(self):
        self.conn.connect()

    def commit(self):
        self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()
