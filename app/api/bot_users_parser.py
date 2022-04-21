from email.policy import default
from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('user_id_tg', required=True)