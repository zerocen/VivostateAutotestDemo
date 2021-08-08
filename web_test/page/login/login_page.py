import os
from utils.data_path_manager import data_path_manager
from web_test.page.base_page import BasePage
from utils.logger import logger


class LoginPage(BasePage):
    page_function_file = os.path.join(data_path_manager.page_data_dir, "login", "login_page_functions.yml")

    def login(self, username, password):
        params = {
            "username": username,
            "password": password
        }
        logger.info(f"Log in TMS. Params={params}")
        self.perform_functions(self.page_function_file, "login", params)
