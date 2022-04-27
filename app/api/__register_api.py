from flask_restful import Api
from . import users_resource, bot_users_resource, bot_auth_resource, lessons_resource, news_resource, articles_resource

def register_api(app):
    api = Api(app)

    # ресурсы для пользователей
    api.add_resource(users_resource.UsersListResource, "/ecol_study_api/users")
    api.add_resource(users_resource.UsersResource, '/ecol_study_api/user/<int:user_id>')

    # апи для пользователей бота
    api.add_resource(bot_users_resource.BotUsersResource, '/ecol_study_api/bot/users/<int:tg_id>')
    api.add_resource(bot_users_resource.BotUsersListResource, '/ecol_study_api/bot/users/')

    # для проверки регистрации пользователя
    api.add_resource(bot_auth_resource.BotAuthResource, "/ecol_study_api/user_login/")

    # регистрация для таблиц в бд на сайт для документации
    api.add_resource(lessons_resource.LessonsResource, '/ecol_study_api/lessons/<int:lesson_id>')
    api.add_resource(lessons_resource.LessonsListResource, '/ecol_study_api/lessons/')

    api.add_resource(articles_resource.ArticlesResource, '/ecol_study_api/articles/<int:article_id>')
    api.add_resource(articles_resource.ArticlesListResource, '/ecol_study_api/articles/')

    api.add_resource(news_resource.NewsResource, '/ecol_study_api/news/<int:news_id>')
    api.add_resource(news_resource.NewsListResource, '/ecol_study_api/news/')