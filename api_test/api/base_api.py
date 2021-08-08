import requests
from utils.configurator import config
from utils.logger import logger


class BaseApi:
    def __init__(self):
        self.base_url = config["app_url"]
        self.proxies = {
            "http": config["proxy"],
            "https": config["proxy"]
        }
        self.session = requests.Session()

    def send_request(self, *args, **kwargs):
        logger.debug(f"Send HTTP Request: {args}, {kwargs}")
        response = self.session.request(*args, **kwargs)
        logger.debug(f"Received HTTP Response: {response.text}")
        return response
