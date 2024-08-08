import sqlite3

import config

from datetime import datetime


class Database:

    def __init__(self):
        self.database = config.DB_NAME

    @property
    def connection(self):
        return sqlite3.connect(self.database)

    def execute(self, sql: str, parameters: tuple = None, operation="fetchone"):
        if not parameters:
            parameters = tuple()

        connection = self.connection
        cursor = connection.cursor()
        cursor.execute(sql, parameters)

        data = None
        if operation == "commit":
            connection.commit()
        else:
            data = getattr(cursor, operation)()
        connection.close()
        return data

    # ---Выборка данных из БД---

    def select_list_of_users(self, **kwargs):
        """
        Получение списка пользователей
        """
        sql = "SELECT id, full_name, age, chat_id FROM users"
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters, "fetchall")

    def check_user_exists(self, chat_id):
        sql = "SELECT COUNT(chat_id) FROM users WHERE chat_id=?"
        exist = self.execute(sql, (chat_id,), "fetchone")[0]
        return bool(exist)

    def select_message_queue(self):
        sql = "SELECT id, chat_id, created_at FROM message_queue"
        sql, parameters = self.format_args(sql, {})
        return self.execute(sql, parameters, "fetchall")

    def add_new_user(self, full_name, age, chat_id):
        user_exists = self.check_user_exists(chat_id)
        if user_exists:
            return "Пользователь с таким Chat ID уже существует"

        sql = "INSERT INTO users (full_name, age, chat_id) VALUES (?,?,?)"
        parameters = (full_name, age, chat_id)
        self.execute(sql, parameters, "commit")

    def add_to_queue(self, chat_id, created_at=None):
        sql = "SELECT COUNT(*) FROM message_queue WHERE chat_id=?"
        exists = self.execute(sql, (chat_id, ), "fetchone")
        exists = bool(exists[0])

        if not created_at:
            created_at = datetime.now()

        if exists:
            sql = "UPDATE message_queue SET created_at=? WHERE chat_id=?"
        else:
            sql = "INSERT INTO message_queue (created_at, chat_id) VALUES (?,?)"

        self.execute(sql, (created_at.strftime("%Y-%m-%d %H:%M:%S"), chat_id), "commit")

    def delete_from_queue(self, chat_id):
        sql = "DELETE FROM message_queue WHERE chat_id=?"
        parameters = (chat_id, )
        self.execute(sql, parameters, "commit")

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([f"{item}=?" for item in parameters])
        return sql, tuple(parameters.values())
