import os
from selenium import webdriver
from utils.data_path_manager import data_path_manager
from web_test.page.base_page import BasePage
from web_test.page.login.login_page import LoginPage
from web_test.page.personalization.personalization_page import PersonalizationPage
from utils.configurator import config
from utils.logger import logger


class App(BasePage):
    page_function_file = os.path.join(data_path_manager.page_data_dir, "app_page_functions.yml")

    def start(self):
        if self.driver is None:
            browser = config["driver_config"]["browser"]
            driver_config = config["driver_config"]

            if browser == "Chrome":
                options = webdriver.ChromeOptions()
                if config["proxy"]:
                    options.add_argument(f'--proxy-server={config["proxy"]}')
                if driver_config["using_headless"]:
                    options.add_argument("--headless")
                if driver_config["debugger"]["using_debugger"]:
                    options.debugger_address = driver_config["debugger"]["debugger_address"]
                self.driver = webdriver.Chrome(options=options)
            elif browser == "Firefox":
                self.driver = webdriver.Firefox()
                options = webdriver.FirefoxOptions()
                if driver_config["using_headless"]:
                    options.add_argument("--headless")
                self.driver = webdriver.Chrome(options=options)
            elif browser == "Edge":
                self.driver = webdriver.Edge()
            elif browser == "Safari":
                self.driver = webdriver.Safari()

            self.driver.maximize_window()
            self.driver.implicitly_wait(config["driver_config"]["default_implicit_waiting_time"])
            self.driver.get(config["app_url"])
        return self

    def stop(self):
        self.driver.quit()

    def current_window_handle(self):
        return self.driver.current_window_handle

    def window_handles(self):
        return self.driver.window_handles

    def current_url(self):
        return self.driver.current_url

    def switch_to_forget_username_password_window(self, window_name):
        self.driver.switch_to.window(window_name)
        return LoginPage(self.driver)

    def go_to_login_page(self):
        logger.info("Go to login page")
        self.driver.get(config["app_url"] + "/tms/login.html")
        return LoginPage(self.driver)

    def go_to_personalization_page(self):
        logger.info("Go to personalization page")
        self.perform_functions(self.page_function_file, "go_to_personalization_page")
        return PersonalizationPage(self.driver)
