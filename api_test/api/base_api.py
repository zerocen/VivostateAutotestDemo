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

    def send_request(self, method: str, url: str, **kwargs):
        logger.debug(f"Send HTTP Request: {method.upper()} {url}, {kwargs}")
        response = self.session.request(method, url, **kwargs)
        logger.debug(f"Received HTTP Response: {response.text}")
        return response
