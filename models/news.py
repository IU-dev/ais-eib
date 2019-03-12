from db import DB


class News:
    def __init__(self, id, title, content, user_id):
        self.id = id
        self.title = title
        self.content = content
        self.user_id = user_id

    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "user_id": self.user_id
        }


class NewsRepository:

    def __init__(self, db: DB):
        self._db = db

    def install(self):
        self._db.execute('''
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title VARCHAR(255),
            content VARCHAR(1024),
            user_id INTEGER
        )
        ''')

    def create(self, news: News):
        cursor = self._db.create_cursor()
        cursor.execute('''
        INSERT INTO news (title, content, user_id)
        VALUES(?,?,?)
        ''', (news.title, news.content, news.user_id))
        news.id = cursor.lastrowid
        cursor.close()
        self._db.commit()

    def get_list(self, limit=0, offset=0):
        cursor = self._db.create_cursor()
        if limit > 0:
            cursor.execute('''SELECT * FROM news ORDER BY id LIMIT ?, ?''', (offset, limit))
        else:
            cursor.execute('''SELECT * FROM news ORDER BY id''')
        data = cursor.fetchall()
        return list(map(self._data_to_model, data))

    def get_last(self, count=3):
        return self.get_list(count, 0)

    def get_by_id(self, id):
        cursor = self._db.create_cursor()
        cursor.execute('''SELECT * FROM news WHERE id=?''', [id])
        data = cursor.fetchone()
        if data:
            return self._data_to_model(data)
        else:
            return None

    def get_by_user_id(self, user_id: int):
        cursor = self._db.create_cursor()
        cursor.execute('''SELECT * FROM news WHERE user_id=?''', [user_id])
        data = cursor.fetchall()
        return map(self._data_to_model, data)

    def update(self, news: News):
        self._db.execute('''
        UPDATE news SET title=?, content=? WHERE id=?
        ''', (news.title, news.content, news.user_id))

    def delete(self, news: News):
        self._db.execute('''
        DELETE FROM news WHERE id=?
        ''', [news.id])

    def _data_to_model(self, data):
        return News(data[0], data[1], data[2], data[3])
