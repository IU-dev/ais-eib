"""
Класс для подключения к базе данных SQLite. Имя файла базы данных передаётся в конструкторе.

Для запросов, которые не требуют получения информации (CREATE TABLE, UPDATE и т.д.) лучше использовать метод execute

Для остальных случаев нужно получить курсор. Если запросы вносили изменени, нужно закрыть курсок (cursor.close()) и
вызвать метод commit()
"""
import sqlite3


class DB:
    def __init__(self, file_name='sqlite.db'):
        self._conn = sqlite3.connect(file_name, check_same_thread=False)

    def create_cursor(self):
        return self._conn.cursor()

    def execute(self, sql, *params, **kparams):
        cursor = self.create_cursor()
        cursor.execute(sql, *params, **kparams)
        cursor.close()
        self._conn.commit()

    def commit(self):
        self._conn.commit()

    def __del__(self):
        self._conn.close()
