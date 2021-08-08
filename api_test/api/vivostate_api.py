from api_test.api.base_api import BaseApi
from utils.configurator import config


class VivostateApi(BaseApi):

    def __init__(self):
        super().__init__()
        user_name = config["account"]["username"]
        password = config["account"]["password"]
        auth_token = self.get_auth_token(user_name, password)
        if auth_token:
            self.session.headers["X-Auth-Token"] = auth_token
        else:
            raise Exception("Failed to get authentication token!")

    def get_auth_token(self, username, password):
        path = "/admin/api/auth/loginEx"
        data = {
            "username": username,
            "password": password
        }
        self.session.headers["Content-Type"] = "application/json; charset=utf-8"
        response = self.send_request("POST", self.base_url + path, json=data)
        if response.status_code == 200:
            auth_token = response.headers["X-Auth-Token"]
            return auth_token
        else:
            return None
