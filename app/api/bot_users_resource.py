from aiogram import Bot
from flask_restful import reqparse, abort, Resource
from flask import jsonify
from data import db_session
from data.bot_users import BotUsers
from .bot_users_parser import parser


def abort_if_user_not_found(tg_id):
    session = db_session.create_session()
    try:
        user = session.query(BotUsers).filter(BotUsers.id_tg_user == tg_id).first()
    except Exception:
        abort(404, message=f"User {tg_id} not found")


class BotUsersResource(Resource):
    def get(self, tg_id):
        abort_if_user_not_found(tg_id)
        return jsonify(
            {
                'success': "Ok"
            }
        )

    def delete(self, tg_id):
        abort_if_user_not_found(tg_id)
        db_sess = db_session.create_session()
        user = db_sess.query(BotUsers).filter(Bot.id_tg_user == tg_id)
        db_sess.delete(user)
        db_sess.commit()
        return jsonify({'success': 'OK'})


class BotUsersListResource(Resource):
    def get(self):
        db_sess = db_session.create_session()
        users = db_sess.query(BotUsers).all()
        return jsonify(
            {
                'users':
                    [item.to_dict(only=(
                        "id", 'id_tg_user'))
                        for item in users]
            }
        )

    def post(self):
        db_sess = db_session.create_session()
        args = parser.parse_args()
        user = BotUsers(
            id_tg_user=args['user_id_tg']
            )
        db_sess.add(user)
        db_sess.commit()
        return jsonify({'success': 'OK'})