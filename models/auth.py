from models.user import UserRepository
from flask import session


class Auth:

    def __init__(self, repository: UserRepository):
        self._repository = repository

    def login(self, login, password):
        user = self._repository.get_by_login(login)
        if user and user.password == password:
            session['user_id'] = user.id
            return True
        return False

    def logout(self):
        session['user_id'] = None

    def get_user(self):
        user_id = session.get('user_id')
        if not user_id:
            return None
        user = self._repository.get_by_id(user_id)
        return user

    def is_authorized(self):
        return bool(session.get('user_id'))
