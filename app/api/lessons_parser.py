from email.policy import default
from flask_restful import reqparse


parser = reqparse.RequestParser()
parser.add_argument('title', required=True)
parser.add_argument('content', default="")
parser.add_argument('user_id', required=True)