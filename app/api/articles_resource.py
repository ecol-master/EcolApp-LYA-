from flask_restful import reqparse, abort, Resource
from flask import jsonify
from data import db_session
from data.articles import Article 
from .articles_parser import parser


def abort_if_article_not_found(article_id):
    session = db_session.create_session()
    article = session.query(Article).get(article_id)
    if not article:
        abort(404, message=f"Article {article_id} not found")


class ArticlesResource(Resource):
    def get(self, article_id):
        abort_if_article_not_found(article_id)
        db_ses = db_session.create_session()
        article = db_ses.query(Article).get(article_id)
        return jsonify(
            {
                'article': article.to_dict(only=(
                    'title', 'user.nickname'))
            }
        )

    def delete(self, article_id):
        abort_if_article_not_found(article_id)
        db_sess = db_session.create_session()
        articles = db_sess.query(Article).get(article_id)
        db_sess.delete(articles)
        db_sess.commit()
        return jsonify({'success': 'OK'})


class ArticlesListResource(Resource):
    def get(self):
        db_sess = db_session.create_session()
        articles = db_sess.query(Article).all()
        return jsonify(
            {
                'articles':
                    [item.to_dict(only=(
                        'title', 'user.nickname'))
                        for item in articles]
            }
        )

    def post(self):
        db_sess = db_session.create_session()
        args = parser.parse_args()
        article = Article(
            title=args["title"],
            text=args["text"],
            user_id=["user_id"]
            )
        db_sess.add(article)
        db_sess.commit()
        return jsonify({'success': 'OK'})