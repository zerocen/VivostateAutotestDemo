import os
import yaml
from utils.data_path_manager import data_path_manager


class Configurator:
    # def __new__(cls):
    #     if not hasattr(Configurator, "instance"):
    #         cls.instance = super().__new__(cls)
    #     return cls.instance

    def __init__(self):
        with open(f"{data_path_manager.project_dir}/config.yml", "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)


config = Configurator().config
username = os.getenv('tms_username')
password = os.getenv('tms_password')
config["account"] = {
    "username": username,
    "password": password
}
