import requests

class DataBaseDispatcher:
    def __init__(self) -> None:
        self.server_api = "http://127.0.0.1:5000/ecol_study_api/"

    def get_users(self):
        req = f"{self.server_api}users"
        response = requests.get(req).json()
        return response
    
    def add_user(self, *args, **kwargs):
        print(f"{args=}")
        print(f"{kwargs=}")
        req = f"{self.server_api}users"
        response = requests.post(req, json={
            "nickname":kwargs["admin_name"], 
            "description":"", 
            "email":kwargs["admin_email"],
            "password":kwargs["admin_password"], 
            "role_id":2
        }).json()        
        return response == {'success': 'OK'}
        

    
    def get_articles(self):
        pass
    
    def get_daily_info(self):
        pass

    