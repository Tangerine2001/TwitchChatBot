import mysql.connector


class DB:
    def __init__(self):
        #   Connect to db
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="SouljaBoy420!",
            database="twitch"
        )
        self.cur = self.conn.cursor()

    def insert(self, tableName: str, values: tuple):
        query = f'INSERT INTO twitch.{tableName} (username, currency, rank_name, hours, first_join, last_join) VALUES (%s, %s, %s, %s, %s, %s)'

        self.cur.execute(query, values)
        self.conn.commit()

    def getLeaderboard(self):
        query = f'SELECT * FROM twitch.users ORDER BY currency LIMIT 5'

        self.cur.execute(query)
        return self.cur.fetchall()

    def close(self):
        self.cur.close()
        self.conn.close()
