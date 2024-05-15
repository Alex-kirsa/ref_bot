import datetime
import os
import sqlite3

from dispather import bot


class UserDb:
    """Work with data from user database"""

    db_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "db.db")

    async def init_user_db(self, user: dict):
        """
        :param user:
        :return:
        """
        with sqlite3.connect(self.db_path) as db_connect:
            cursor = db_connect.cursor()
            query = """SELECT * FROM users WHERE User_id=?"""
            cursor.execute(query, [user.get('id')])
            answer = cursor.fetchall()
            if not answer:
                query = """INSERT INTO users(User_id,Active,Invited_by,Data,User_name) VALUES(?,?,?,?,?)"""
                cursor.execute(query, [user['id'], True, user['invited_by'],
                                       datetime.datetime.now().date(), user['username']])
                db_connect.commit()

    async def check_user(self, user_id):
        with sqlite3.connect(self.db_path) as db_connect:
            cursor = db_connect.cursor()
            query = """SELECT * FROM users WHERE User_id=?"""
            cursor.execute(query, [user_id])
            answer = cursor.fetchall()
            return answer

    def add_task(self, title, text, photo, goal):
        with sqlite3.connect(self.db_path) as db_connect:
            cursor = db_connect.cursor()
            cursor.execute("INSERT INTO tasks (title, text, photo, goal, active) VALUES (?, ?, ?, ?, ?)",
                           (title, text, photo, goal, True))
            db_connect.commit()

    def active_tasks(self):
        with sqlite3.connect(self.db_path) as db_connect:
            cursor = db_connect.cursor()
            query = """SELECT * FROM tasks WHERE active=1"""
            cursor.execute(query,)
            answer = cursor.fetchone()
            return answer

    def del_task(self):
        with sqlite3.connect(self.db_path) as db_connect:
            cursor = db_connect.cursor()
            query = """UPDATE tasks SET active=0"""
            cursor.execute(query,)
