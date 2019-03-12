from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import PasswordField
from wtforms import FileField
from wtforms import SubmitField
from wtforms.validators import DataRequired
from models.user import UserRepository
from models.user import User
from models.record import Record
from models.record import RecordRepository
from werkzeug.security import generate_password_hash
import os


class RecordCreateForm(FlaskForm):
    patient = StringField('ИД пациента', validators=[DataRequired()])
    doctor = StringField('ИД врача', validators=[DataRequired()])
    header = StringField('Заголовок', validators=[DataRequired()])
    body = StringField('Текст записи', validators=[DataRequired()])

    submit = SubmitField('Создать запись')

    def __init__(self, repository: RecordRepository):
        super(RecordCreateForm, self).__init__()
        self._repository = repository

    def create_user(self):
        patient = self.patient.data
        doctor = self.doctor.data
        header = self.header.data
        body = self.body.data
        record = Record(None, patient, doctor, header, body)
        self._repository.create(record)
