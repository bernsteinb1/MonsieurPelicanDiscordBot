import sqlite3
import discord

conn = sqlite3.connect("games.db")

class DailyGame:
    def __init__(self, game: str):
        self.game = game
        self.cur = conn.cursor()
        self.cur.execute(f"CREATE TABLE IF NOT EXISTS {game} (date TEXT, user_id INTEGER, message_id INTEGER, score INTEGER, PRIMARY KEY (date, user_id))")
    
    def insert_score(self, date, user_id, message_id, score):
        self.cur.execute(f"SELECT 1 FROM {self.game} WHERE date = ? AND user_id = ?", (date, user_id))
        if self.cur.fetchone() is not None:
            return False
        self.cur.execute(f"INSERT INTO {self.game} (date, user_id, message_id, score) VALUES (?, ?, ?, ?);", (date, user_id, message_id, score))
        conn.commit()
        return True
    
    def get_record(self, user_1, user_2):
        query = f'SELECT COUNT(*) AS total,\
                 COUNT(CASE WHEN x.score > y.score THEN 1 END) AS wins,\
                 COUNT(CASE WHEN y.score > x.score THEN 1 END) AS losses,\
                 COUNT(CASE WHEN x.score = y.score THEN 1 END) AS ties\
                 FROM {self.game} AS x\
                 JOIN {self.game} AS y USING (date)\
                 WHERE x.user_id = ? AND y.user_id = ?;'
        self.cur.execute(query, (user_1, user_2))
        return self.cur.fetchone()