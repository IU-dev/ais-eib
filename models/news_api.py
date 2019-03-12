from flask_restful import Resource
from flask_restful import reqparse
from flask import jsonify
from flask import abort
from models.news import NewsRepository
from models.news import News
from models.auth import Auth

news_parser = reqparse.RequestParser()
news_parser.add_argument('title', required=True)
news_parser.add_argument('content', required=True)


class NewsListApi(Resource):
    def __init__(self, repository: NewsRepository, auth: Auth):
        super(NewsListApi, self).__init__()
        self._repository = repository
        self._auth = auth

    def get(self):
        news = self._repository.get_list()
        return jsonify(news)

    def post(self):
        if not self._auth.is_authorized():
            abort(401)
        args = news_parser.parse_args()
        news = News(None, args['title'], args['content'], self._auth.get_user().id)
        self._repository.create(news)
        return jsonify(news)


class NewsApi(Resource):

    def __init__(self, repository: NewsRepository, auth: Auth):
        super(NewsApi, self).__init__()
        self._repository = repository
        self._auth = auth

    def get(self, id: int):
        news = self._repository.get_by_id(id)
        if not news:
            abort(404)
        return jsonify(news)

    def delete(self, id: int):
        if not self._auth.is_authorized():
            abort(401)
        news = self._repository.get_by_id(id)
        if news.user_id != self._auth.get_user().id:
            abort(403)
        self._repository.delete(news)
        return jsonify({"deleted": True})
