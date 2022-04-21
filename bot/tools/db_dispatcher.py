from ast import arg
import requests

class DataBaseDispatcher:
    def __init__(self) -> None:
        self.server_api = "http://127.0.0.1:5000/ecol_study_api/"
        self.api_key = "123Dfg5HYTL4**93"
    def get_users(self):
        req = f"{self.server_api}users"
        response = requests.get(req).json()
        return response
    
    def add_user(self, **kwargs):
        req = f"{self.server_api}users"
        response = requests.post(req, json={
            "nickname":kwargs["admin_name"], 
            "description":"", 
            "email":kwargs["admin_email"],
            "password":kwargs["admin_password"], 
            "role_id":2
        }).json()        
        return response == {'success': 'OK'}
        

    def login_user(self, *args, **kwargs):
        req = f"{self.server_api}users/{self.api_key}"
        response =requests.get(req).json()
        for data in response:
            if data["email" == kwargs["user_email"]] and data["password"] == kwargs["user_password"]:
                pass
        return response

    def get_articles(self):
        pass
    
    def get_daily_info(self):
        pass

    