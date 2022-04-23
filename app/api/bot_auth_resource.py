from flask_restful import reqparse, abort, Resource
from flask import jsonify
from data import db_session
from data.users import User
from .bot_auth_parser import parser


class BotAuthResource(Resource):
    def post(self):
        args = parser.parse_args()
        user_email, user_password = args["email"], args["password"]
        session = db_session.create_session()
        user = session.query(User).filter(User.email == user_email, User.password == user_password).first()
        if user:
                return jsonify(
                    {
                        'success': user.id 
                    }
                )
        else:
            return jsonify(
                    {
                        'failed': "not found"
                    }
                )