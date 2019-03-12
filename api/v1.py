from models.news_api import NewsListApi
from models.news_api import NewsApi
from models.news import NewsRepository
from models.auth import Auth
from flask_restful import Api
from flask import Flask


def init(app: Flask, repository: NewsRepository, auth: Auth):
    api = Api(app)
    api.add_resource(NewsListApi, '/api/v1/news', resource_class_args=[repository, auth])
    api.add_resource(NewsApi, '/api/v1/news/<int:id>', resource_class_args=[repository, auth])
