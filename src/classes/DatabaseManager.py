from assets import SQL_config as config
from typing import Any,Sequence
import pathlib
import sqlite3
import logging

log = logging.getLogger(__name__)

class DatabaseManager:

    def __init__(self) -> None:

        #   Path Variables
        self._set_file_path_variables()

        # connection
        self.connection: sqlite3.Connection = self._get_connection()
        
        # Makes tables if they don't exist
        self._build_db()

    # base

    def _build_db(self) -> None:
        WIREFRAME:str = config.LOG_DATABASE_WIREFRAME
        self.execute_script(WIREFRAME)

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.DB_PATH / self.FILE_NAME)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA foreign_keys=ON")
        return conn

    def _set_file_path_variables(self) -> None:
        self.DB_PATH:pathlib.Path = pathlib.Path(config.DATABASE_PATH_STR)
        self.FILE_NAME:str = config.LOG_DATABASE_FILE_NAME

    # SQL query executers
    
    def fetch_data(self, sql_query:str, parameters:Sequence[Any]=()) -> list[Any]:
        """Executes a sql query and returns the result <p>
        Won't commit to the database"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql_query, parameters)
            return cursor.fetchall()

        except Exception as e:
            log.warning("couldn't make query: %s\nexception: %s", sql_query, e)
            return []

    def make_query(self, sql_query:str, parameters:Sequence[Any]=()) -> list[Any]:
        """Executes a sql query and returns the result <p>
        Will commit to the database"""
        with self.connection as conn: # "with" auto commits when the function exits its scope
            cursor = conn.cursor()
            cursor.execute(sql_query, parameters)
            return cursor.fetchall()

    def execute_script(self, sql_queries:str) -> list[Any]:
        """Executes a series of sql queries and returns the result <p>
        Will commit to the database"""
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.executescript(sql_queries) # executescript autocommits to database
            return cursor.fetchall()
    
        