from flask_restful import Api
from . import users_resource


def register_api(app):
    api = Api(app)

    # ресурсы для пользователей
    api.add_resource(users_resource.UsersListResource, '/ecol_study_api/users')
    api.add_resource(users_resource.UsersResource, '/ecol_study_api/users/<int:user_id>')
    