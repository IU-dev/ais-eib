from db import DB


class Record():
    def __init__(self, id, patient, doctor, header, body):
        self.id = id
        self.patient = patient
        self.doctor = doctor
        self.header = header
        self.body = body


class RecordRepository():

    def __init__(self, db: DB):
        self._db = db

    def install(self):
        self._db.execute('''
        CREATE TABLE IF NOT EXISTS record (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient VARCHAR(255),
            doctor VARCHAR(255),
            header VARCHAR(255),
            body VARCHAR(4096)      
        )
        ''')

    def create(self, record: Record):
        self._db.execute('''
        INSERT INTO record (patient, doctor, header, body)
        VALUES(?,?,?,?,?)
        ''', (record.patient, record.doctor, record.header, record.body))

    def get_list(self, limit=0, offset=0):
        cursor = self._db.create_cursor()
        if limit > 0:
            cursor.execute('''SELECT * FROM record ORDER BY id  LIMIT ?, ?''', (offset, limit))
        else:
            cursor.execute('''SELECT * FROM record ORDER BY id ''')

        data = cursor.fetchall()
        return list(map(self._data_to_model, data))

    def get_list_for_patient(self, patient):
        cursor = self._db.create_cursor()
        cursor.execute('''SELECT * FROM record WHERE patient = ? ORDER BY id DESC''', (patient))
        data = cursor.fetchall()
        return list(map(self._data_to_model, data))

    def get_by_id(self, id):
        cursor = self._db.create_cursor()
        cursor.execute('''SELECT * FROM record WHERE id=?''', [id])
        data = cursor.fetchone()
        if not data:
            return None
        return self._data_to_model(data)

    def delete(self, record: Record):
        self._db.execute('''
        DELETE FROM record WHERE id=?
        ''', [record.id])

    def _data_to_model(self, data):
        return Record(data[0], data[1], data[2], data[3], data[4])
