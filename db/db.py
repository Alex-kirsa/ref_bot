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

    def add_task(self, title, text, photo, goal, done_text):
        self.del_task()
        with sqlite3.connect(self.db_path) as db_connect:
            cursor = db_connect.cursor()
            cursor.execute("INSERT INTO tasks (title, text, photo, goal, active, done_text) VALUES (?, ?, ?, ?, ?,?)",
                           (title, text, photo, goal, True, done_text))
            db_connect.commit()

    def add_referral_task(self, user_id, task, inviter):
        with sqlite3.connect(self.db_path) as db_connect:
            cursor = db_connect.cursor()
            cursor.execute("SELECT * FROM invited WHERE User_id=? and task_id=? and inviter=?",
                           (user_id, task, inviter))
            check = cursor.fetchall()
            if not check:
                cursor.execute("INSERT INTO invited (User_id, task_id, inviter) VALUES (?, ?, ?)",
                               (user_id, task, inviter))
                db_connect.commit()

    def active_tasks(self):
        with sqlite3.connect(self.db_path) as db_connect:
            cursor = db_connect.cursor()
            query = """SELECT * FROM tasks WHERE active=1"""
            cursor.execute(query, )
            answer = cursor.fetchone()
            return answer

    def del_task(self):
        with sqlite3.connect(self.db_path) as db_connect:
            cursor = db_connect.cursor()
            query = """UPDATE tasks SET active=0"""
            cursor.execute(query, )
            query = """UPDATE user_tasks SET active=0"""
            cursor.execute(query, )

    def user_task(self, data: list):
        with sqlite3.connect(self.db_path) as db_connect:
            cursor = db_connect.cursor()
            query = """SELECT * FROM user_tasks WHERE  User_id=? and task_id=? and active=True"""
            cursor.execute(query, data)
            user_task = cursor.fetchone()
            query = """SELECT COUNT(*) FROM invited WHERE  inviter=? and task_id=?"""
            cursor.execute(query, data)
            user_task_inviter = cursor.fetchone()[0]
            if not user_task:
                query = """INSERT INTO user_tasks(User_id, task_id) VALUES(?,?)"""
                cursor.execute(query, data)
            return user_task, user_task_inviter

    def mailing(self, task_id=None):
        with sqlite3.connect(self.db_path) as db_connect:
            cursor = db_connect.cursor()
            if task_id:
                query = """SELECT User_id FROM user_tasks WHERE task_id=?"""
                cursor.execute(query, [task_id])
                users = cursor.fetchall()
                return users
            query = """SELECT User_id FROM Users"""
            cursor.execute(query)
            users = cursor.fetchall()
            return users
