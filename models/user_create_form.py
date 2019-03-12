from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import PasswordField
from wtforms import FileField
from wtforms import SubmitField
from wtforms.validators import DataRequired
from models.user import UserRepository
from models.user import User
from werkzeug.security import generate_password_hash
import os


class UserCreateForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    display = StringField('Отображаемое имя', validators=[DataRequired()])
    position = StringField('Должность', validators=[DataRequired()])

    submit = SubmitField('Создать')

    def __init__(self, repository: UserRepository):
        super(UserCreateForm, self).__init__()
        self._repository = repository

    def create_user(self):
        login = self.login.data
        password = self.password.data
        display = self.display.data
        position = self.position.data
        user = User(None, login, password, display, position)
        self._repository.create(user)
