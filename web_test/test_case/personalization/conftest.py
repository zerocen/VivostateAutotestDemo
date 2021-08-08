import allure
import pytest
from utils.configurator import config


@pytest.fixture(name="login", scope="package", autouse=True)
def login(app):
    with allure.step("Log in to TMS"):
        login_page = app.go_to_login_page()
        yield login_page.login(config["account"]["username"], config["account"]["password"])
