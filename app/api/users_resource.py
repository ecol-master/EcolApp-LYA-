from flask_restful import reqparse, abort, Resource
from flask import jsonify
from data import db_session
from data.users import User
from .users_parser import parser


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")


admins_keys = ["123Dfg5HYTL4**93"]

class UsersResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        db_ses = db_session.create_session()
        user = db_ses.query(User).get(user_id)
        return jsonify(
            {
                'user': user.to_dict(only=(
                    'nickname', 'email'))
            }
        )

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        db_sess = db_session.create_session()
        user = db_sess.query(User).get(user_id)
        db_sess.delete(user)
        db_sess.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self, api_key=0):
        db_sess = db_session.create_session()
        users = db_sess.query(User).all()

        if api_key in admins_keys:
            return jsonify(
                {
                    'users':
                        [item.to_dict(only=(
                            'nickname', 'email', "password"))
                            for item in users]
                }
            )
        else:
            return jsonify(
                {
                    'users':
                        [item.to_dict(only=(
                            'nickname', 'email'))
                            for item in users]
                }
            )

    def post(self, api_key=0):
        db_sess = db_session.create_session()
        args = parser.parse_args()
        user = User(
            nickname=args["nickname"],
            description=args["description"],
            email=args["email"],
            password=args["password"],
            role_id=args["role_id"]
            )
        db_sess.add(user)
        user.set_password(user.password)
        db_sess.commit()
        return jsonify({'success': 'OK'})