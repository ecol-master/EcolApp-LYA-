from flask_restful import reqparse, abort, Resource
from flask import jsonify
from data import db_session
from data.bot_users import BotUsers
from .bot_users_parser import parser


def abort_if_user_not_found(tg_id):
    session = db_session.create_session()
    try:
        if session.query(BotUsers).filter(BotUsers.id_tg_user == tg_id).first():
            pass
        else:
            raise Exception
    except Exception:
        abort(404, message=f"not found")


class BotUsersResource(Resource):
    def get(self, tg_id):
        abort_if_user_not_found(tg_id)
        db_sess = db_session.create_session()
        user = db_sess.query(BotUsers).filter(BotUsers.id_tg_user == tg_id).first()
        return jsonify({
            "Name":user.account.nickname,
            "description":user.account.description,
            "data_registration":user.data_register
        })


    def delete(self, tg_id):
        abort_if_user_not_found(tg_id)
        db_sess = db_session.create_session()
        user = db_sess.query(BotUsers).filter(BotUsers.id_tg_user == tg_id).first()
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
    
    def check_user(self, tg_id, account_id):
        session = db_session.create_session()
        user = session.query(BotUsers).filter(BotUsers.id_tg_user == tg_id).first()
        if user:
            user.account_id = account_id
            session.commit(user)
            return {"success":"user was updated"}
        else:
            bot_user = BotUsers(
            id_tg_user=tg_id,
            account_id=account_id
        )
            session.add(bot_user)
            session.commit()
            return {"success":"user was added"}

    def post(self):
        args = parser.parse_args()
        result = self.check_user(args["user_id_tg"], args["account_id"])
        return jsonify(result)