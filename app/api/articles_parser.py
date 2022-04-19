from email.policy import default
from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('nickname', required=True)
parser.add_argument('description', default="")
parser.add_argument('email', required=True)
parser.add_argument('password', required=True)
parser.add_argument('role_id', default=1)