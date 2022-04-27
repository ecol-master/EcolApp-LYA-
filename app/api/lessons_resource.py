from flask_restful import reqparse, abort, Resource
from flask import jsonify
from data import db_session
from data.lessons import Lesson 
from .articles_parser import parser


def abort_if_lesson_not_found(lesson_id):
    session = db_session.create_session()
    lesson = session.query(Lesson).get(lesson_id)
    if not lesson:
        abort(404, message=f"Article {lesson_id} not found")


class LessonsResource(Resource):
    def get(self, lesson_id):
        abort_if_lesson_not_found(lesson_id)
        db_ses = db_session.create_session()
        article = db_ses.query(Lesson).get(lesson_id)
        return jsonify(
            {
                'lesson': article.to_dict(only=(
                    'title', 'description'))
            }
        )


class LessonsListResource(Resource):
    def get(self):
        db_sess = db_session.create_session()
        lessons = db_sess.query(Lesson).all()
        return jsonify(
            {
                'lessons':
                    [item.to_dict(only=(
                        'title', 'description'))
                        for item in lessons]
            }
        )
