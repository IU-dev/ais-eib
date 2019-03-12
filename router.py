"""
Маршрутизатор
"""
from flask import Flask
from flask import render_template as flask_render_template
from flask import redirect
from flask import request
from flask import abort
from db import DB
from models.news import NewsRepository
from models.news import News
from models.user import UserRepository
from models.user_create_form import UserCreateForm
from models.auth import Auth
from models.patient import Patient
from models.patient import PatientRepository
from models.patient_create_form import PatientCreateForm
from models.record import Record
from models.record import RecordRepository
from models.record_create_form import RecordCreateForm
from api.v1 import init as init_api_v1


# Инициализирует маршруты для маршрутизатора и определяет обработчики запросов
def init_route(app: Flask, db: DB):
    # Инициализация зависимостей для обработчиков
    news_repository = NewsRepository(db)
    user_repository = UserRepository(db)
    patient_repository = PatientRepository(db)
    record_repository = RecordRepository(db)
    auth = Auth(user_repository)

    # Переопределение стандартного рендера, добавляет параметр auth_user
    def render_template(*args, **kwargs):
        kwargs['auth_user'] = auth.get_user()
        return flask_render_template(*args, **kwargs)

    #Инициализация маршутов для API
    init_api_v1(app, news_repository, auth)

    @app.route('/')
    @app.route('/index')
    def index():
        last_news = news_repository.get_last(10)
        return render_template(
            'index.html',
            title='Главная | АИС ЭИБ',
            last_news=last_news
        )

    @app.route('/install')
    def install():
        news_repository.install()
        user_repository.install()
        patient_repository.install()
        return render_template(
            'install-success.html',
            title="Успешно | Установщик АИС ЭИБ"
        )

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        has_error = False
        login = ''
        if request.method == 'POST':
            login = request.form['login']
            if auth.login(login, request.form['password']):
                return redirect('/')
            else:
                has_error = True
        return render_template(
            'login.html',
            title='Вход | АИС ЭИБ',
            login=login,
            has_error=has_error
        )

    @app.route('/logout', methods=['GET'])
    def logout():
        auth.logout()
        return redirect('/')

    @app.route('/user', methods=['GET'])
    def user_list():
        user_list = user_repository.get_list()
        return render_template(
            'user-list.html',
            title='Список пользователей | АИС ЭИБ',
            user_list=user_list
        )

    @app.route('/user/create', methods=['GET', 'POST'])
    def user_create_form():
        form = UserCreateForm(user_repository)
        if form.validate_on_submit():
            form.create_user()
            return redirect('/user')
        return render_template(
            'user-create.html',
            title='Создать пользователя | АИС ЭИБ',
            form=form
        )

    @app.route('/record', methods=['GET'])
    def record_list():
        record_list = record_repository.get_list()
        return render_template(
            'record-list.html',
            title='Список записей | АИС ЭИБ',
            record_list=record_list
        )

    @app.route('/record/create', methods=['GET', 'POST'])
    def record_create_form():
        form = RecordCreateForm(record_repository)
        if form.validate_on_submit():
            form.create_user()
            return redirect('/record')
        return render_template(
            'record-create.html',
            title='Создать запись | АИС ЭИБ',
            form=form
        )

    @app.route('/user/delete/<int:id>')
    def user_delete(id: int):
        user = user_repository.get_by_id(id)
        user_repository.delete(user)
        return redirect('/user')

    @app.route('/patient', methods=['GET'])
    def patient_list():
        patient_list = patient_repository.get_list()
        return render_template(
            'patient-list.html',
            title='Список пациентов | АИС ЭИБ',
            patient_list=patient_list
        )

    @app.route('/patient/create', methods=['GET', 'POST'])
    def patient_create_form():
        form = PatientCreateForm(patient_repository)
        if form.validate_on_submit():
            form.create_patient()
            return redirect('/patient')
        return render_template(
            'patient-create.html',
            title='Создать пациента | АИС ЭИБ',
            form=form
        )

    @app.route('/patient/delete/<int:id>')
    def patient_delete(id: int):
        patient = patient_repository.get_by_id(id)
        patient_repository.delete(patient)
        return redirect('/patient')

    @app.route('/news', methods=['GET'])
    def news_list():
        news_list = news_repository.get_list()
        return render_template(
            'news-list.html',
            title="Новости | АИС ЭИБ",
            news_list=news_list
        )

    @app.route('/news/create', methods=['GET'])
    def news_create_form():
        return render_template(
            'news-create.html',
            title="Новая новость | АИС ЭИБ"
        )

    @app.route('/news/create', methods=['POST'])
    def news_create():
        if not auth.is_authorized():
            return redirect('/login')
        news = News(None, request.form['title'], request.form['content'], auth.get_user().id)
        news_repository.create(news)
        return redirect('/news')

    @app.route('/news/<int:id>')
    def news_view(id: int):
        news = news_repository.get_by_id(id)
        user = user_repository.get_by_id(news.user_id)
        return render_template(
            'news-view.html',
            title="Просмотр новости | АИС ЭИБ",
            news=news,
            user=user
        )

    @app.route('/news/delete/<int:id>')
    def news_delete(id: int):
        news = news_repository.get_by_id(id)
        if news.user_id != auth.get_user().id:
            abort(403)
        news_repository.delete(news)
        return redirect('/news')
