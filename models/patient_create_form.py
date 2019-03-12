from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import PasswordField
from wtforms import FileField
from wtforms import SubmitField
from wtforms.validators import DataRequired
from models.patient import PatientRepository
from models.patient import Patient
from werkzeug.security import generate_password_hash
import os


class PatientCreateForm(FlaskForm):
    name = StringField('ФИО', validators=[DataRequired()])
    address = StringField('Адрес', validators=[DataRequired()])
    uchastok = StringField('Участок', validators=[DataRequired()])
    cardno = StringField('Номер бумажной карты', validators=[DataRequired()])

    submit = SubmitField('Создать')

    def __init__(self, repository: PatientRepository):
        super(PatientCreateForm, self).__init__()
        self._repository = repository

    def create_patient(self):
        name = self.name.data
        address = self.address.data
        uchastok = self.uchastok.data
        cardno = self.cardno.data
        patient = Patient(None, name, address, uchastok, cardno)
        self._repository.create(patient)
