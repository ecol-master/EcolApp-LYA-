from ast import arg
import requests

class DataBaseDispatcher:
    def __init__(self) -> None:
        self.server_api = "http://127.0.0.1:5000/ecol_study_api"

    def get_users(self):
        req = f"{self.server_api}users"
        response = requests.get(req).json()
        return response
    
    def add_user(self, **kwargs):
        req = f"{self.server_api}/users"
        response = requests.post(req, json={
            "nickname":kwargs["admin_name"], 
            "description":"", 
            "email":kwargs["admin_email"],
            "password":kwargs["admin_password"], 
            "role_id":2
        }).json()        
        return response == {'success': 'OK'}
        

    def check_login(self, email, password):
        req = f"{self.server_api}/user_login/"
        response =requests.post(req, json={
            "email":email, "password":password
        }).json()
        return response

    def login_user(self, *args, **kwargs):
        # отправление запроса на сервер для получения пользователя
        email, password = kwargs["user_email"], kwargs["user_password"]
        response = self.check_login(email, password)
        match response:
            case {'success': int(id)}:
                req = f"{self.server_api}/bot/users/"
                response_bot = requests.post(req, json={
                    "user_id_tg":args[0], "account_id":id
                }).json()
                return response_bot
            case _:
                return response

    def get_user_info(self, tg_id):
        req = f"{self.server_api}/bot/users/{tg_id}"
        response = requests.get(req).json()
        return response
        
    def check_bot_user(self, tg_id):
        req = f"{self.server_api}/bot/users/{tg_id}"
        response = requests.get(req).json()
        return response

    def delete_bot_user(self, tg_id):
        req = f"{self.server_api}/bot/users/{tg_id}"
        response = requests.delete(req).json()
        return response
    
    def get_daily_info(self):
        pass

    