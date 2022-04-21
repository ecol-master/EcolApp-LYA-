from flask_restful import Api
from . import users_resource, bot_users_resource


def register_api(app):
    api = Api(app)

    # ресурсы для пользователей
    api.add_resource(users_resource.UsersListResource, "/ecol_study_api/users", '/ecol_study_api/users/<api_key>')
    api.add_resource(users_resource.UsersResource, '/ecol_study_api/user/<int:user_id>')

    # апи для пользователей бота
    api.add_resource(bot_users_resource.BotUsersResource, '/ecol_study_api/bot/users')
    api.add_resource(bot_users_resource.BotUsersListResource, '/ecol_study_api/bot/users/<int:tg_id>')