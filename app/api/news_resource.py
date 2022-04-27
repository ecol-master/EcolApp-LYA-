from flask_restful import reqparse, abort, Resource
from flask import jsonify
from data import db_session
from data.news import News
from .articles_parser import parser


def abort_if_news_not_found(news_id):
    session = db_session.create_session()
    news = session.query(News).get(news_id)
    if not news:
        abort(404, message=f"Article {news_id} not found")


class NewsResource(Resource):
    def get(self, news_id):
        abort_if_news_not_found(news_id)
        db_ses = db_session.create_session()
        news = db_ses.query(News).get(news_id)
        return jsonify(
            {
                'news': news.to_dict(only=(
                    'title', 'content', 'user.nickname'))
            }
        )

    def delete(self, news_id):
        abort_if_news_not_found(news_id)
        db_sess = db_session.create_session()
        news = db_sess.query(News).get(news_id)
        db_sess.delete(news)
        db_sess.commit()
        return jsonify({'success': 'OK'})


class NewsListResource(Resource):
    def get(self):
        db_sess = db_session.create_session()
        news = db_sess.query(News).all()
        return jsonify(
            {
                'news':
                    [item.to_dict(only=(
                        'title', 'content', 'user.nickname'))
                        for item in news]
            }
        )

    def post(self):
        db_sess = db_session.create_session()
        args = parser.parse_args()
        news = News(
            title=args["title"],
            content=args["content"],
            user_id=["user_id"]
            )
        db_sess.add(news)
        db_sess.commit()
        return jsonify({'success': 'OK'})