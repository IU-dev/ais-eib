from db import DB


class User():
    def __init__(self, id, login, password, display, position):
        self.id = id
        self.login = login
        self.password = password
        self.display = display
        self.position = position


class UserRepository():

    def __init__(self, db: DB):
        self._db = db

    def install(self):
        self._db.execute('''
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login VARCHAR(255),
            password VARCHAR(255),
            display VARCHAR(255),
            position VARCHAR(255)       
        )
        ''')

    def create(self, user: User):
        self._db.execute('''
        INSERT INTO user (login, password, display, position)
        VALUES(?,?,?,?)
        ''', (user.login, user.password, user.display, user.position))

    def get_list(self, limit=0, offset=0):
        cursor = self._db.create_cursor()
        if limit > 0:
            cursor.execute('''SELECT * FROM user ORDER BY id  LIMIT ?, ?''', (offset, limit))
        else:
            cursor.execute('''SELECT * FROM user ORDER BY id ''')

        data = cursor.fetchall()
        return list(map(self._data_to_model, data))

    def get_last(self, count=3):
        return self.get_list(count, 0)

    def get_by_id(self, id):
        cursor = self._db.create_cursor()
        cursor.execute('''SELECT * FROM user WHERE id=?''', [id])
        data = cursor.fetchone()
        if not data:
            return None
        return self._data_to_model(data)

    def get_by_login(self, login):
        cursor = self._db.create_cursor()
        cursor.execute('''SELECT * FROM user WHERE login=?''', [login])
        data = cursor.fetchone()
        if not data:
            return None
        return self._data_to_model(data)

    def update(self, user: User):
        self._db.execute('''
        UPDATE news SET password=? WHERE id=?
        ''', [user.password])

    def delete(self, user: User):
        self._db.execute('''
        DELETE FROM user WHERE id=?
        ''', [user.id])

    def _data_to_model(self, data):
        return User(data[0], data[1], data[2], data[3], data[4])
