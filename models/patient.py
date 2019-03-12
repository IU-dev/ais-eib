from db import DB


class Patient():
    def __init__(self, id, name, address, uchastok, cardno):
        self.id = id
        self.name = name
        self.address = address
        self.uchastok = uchastok
        self.cardno = cardno


class PatientRepository():

    def __init__(self, db: DB):
        self._db = db

    def install(self):
        self._db.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255),
            address VARCHAR(255),
            uchastok VARCHAR(255),
            cardno VARCHAR(255)       
        )
        ''')

    def create(self, patient: Patient):
        self._db.execute('''
        INSERT INTO patients (name, address, uchastok, cardno)
        VALUES(?,?,?,?)
        ''', (patient.name, patient.address , patient.uchastok, patient.cardno))

    def get_list(self, limit=0, offset=0):
        cursor = self._db.create_cursor()
        if limit > 0:
            cursor.execute('''SELECT * FROM patients ORDER BY id  LIMIT ?, ?''', (offset, limit))
        else:
            cursor.execute('''SELECT * FROM patients ORDER BY id ''')

        data = cursor.fetchall()
        return list(map(self._data_to_model, data))

    def get_last(self, count=3):
        return self.get_list(count, 0)

    def get_by_id(self, id):
        cursor = self._db.create_cursor()
        cursor.execute('''SELECT * FROM patients WHERE id=?''', [id])
        data = cursor.fetchone()
        if not data:
            return None
        return self._data_to_model(data)

    def get_by_cardno(self, cardno):
        cursor = self._db.create_cursor()
        cursor.execute('''SELECT * FROM patients WHERE cardno=?''', [cardno])
        data = cursor.fetchone()
        if not data:
            return None
        return self._data_to_model(data)

    def delete(self, patient: Patient):
        self._db.execute('''
        DELETE FROM patients WHERE id=?
        ''', [patient.id])

    def _data_to_model(self, data):
        return Patient(data[0], data[1], data[2], data[3], data[4])
