import os
import sqlite3


def _create_tables():
    create = __CreateTable()
    create.create_tables()


class __CreateTable:
    def __init__(self):
        self.db_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "db.db")
        self.__table_queries = {
            "users": '''
                CREATE TABLE IF NOT EXISTS Users
                (Id INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT,
                User_id INTEGER,
                Active INTEGER, 
                Invited_by INTEGER,
                Data DATE,
                User_name TEXT
                );''',
            "tasks": '''
                CREATE TABLE IF NOT EXISTS tasks
                (Id INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                text TEXT,
                photo TEXT,
                goal INTEGER,
                active BOOL,
                done_text TEXT
                );''',
            "user_tasks": '''
                CREATE TABLE IF NOT EXISTS user_tasks
                (Id INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT,
                User_id INTEGER,
                task_id INTEGER,
                active BOOL DEFAULT True
                );''',
            'invited': '''
            CREATE TABLE IF NOT EXISTS invited
                (Id INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT,
                User_id INTEGER,
                task_id INTEGER,
                inviter INTEGER
                );
            '''
        }

    def create_tables(self):
        with sqlite3.connect(self.db_path) as db:
            cursor = db.cursor()
            for query in self.__table_queries.values():
                cursor.execute(query)
