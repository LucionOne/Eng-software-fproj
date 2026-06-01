from typing import Any
from assets import SQL_config as config
import pathlib
import sqlite3

class DatabaseManager:
    def __init__(self) -> None:

        #   Path Variables
        self.DB_PATH:pathlib.Path = pathlib.Path(config.DATABASE_PATH_STR)
        self.FILE_NAME:str =        config.LOG_DATABASE_FILE_NAME
        self.WIREFRAME:str =        config.LOG_DATABASE_WIREFRAME

        # connection
        self.connection: sqlite3.Connection = self.get_connection()
        
        # Makes tables
        self.build_db()


    def build_db(self) -> None:
        self.make_query(self.WIREFRAME)

    # base

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.DB_PATH / self.FILE_NAME)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA foreign_keys=ON")
        return conn

    def make_query(self, query:str) -> list[Any]:
        with self.connection as conn:
            conn.cursor().executescript(query)
            return conn.cursor().fetchall()

    # SQL queries

    
        