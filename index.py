"""
Точка входа

Здесь инициализируются все настройки, подключения к БД, приложение flask и маршрутизатор (router)

После инициализации запускается вебсервер
"""

from flask import Flask
from router import init_route
from db import DB
from util.json_encoder import JSONEncoder

db = DB('news.db')

app = Flask(__name__)
app.secret_key = 'news service secret key'
app.config['SESSION_TYPE'] = 'filesystem'
app.json_encoder = JSONEncoder
init_route(app, db)

app.run(port=8000, host='127.0.0.1')
