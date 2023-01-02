import sqlite3

# sqlite3のdbとやりとりをするクラス
class SqliteConnection:
    conn = None

    @classmethod
    def set_connection(cls):
        cls.conn = sqlite3.connect("./db/splabot.db")

    @classmethod
    def get_connection(cls):
        return cls.conn

    @classmethod
    def close(cls):
        if cls.conn != None:
            cls.conn.close()
