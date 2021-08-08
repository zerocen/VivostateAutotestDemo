import pytest
from web_test.page.app import App


@pytest.fixture(name="app", scope="session")
def start_app():
    app = App().start()
    yield app
    app.stop()


# def pytest_assertrepr_compare(config, op, left, right):
#     left_name, right_name = inspect.stack()[7].code_context[0].lstrip().lstrip('assert').rstrip('\n').split(op)
#     pytest_output = assertrepr_compare(config, op, left, right)
#     logging.debug("{0} is\n {1}".format(left_name, left))
#     logging.debug("{0} is\n {1}".format(right_name, right))
#     with allure.step("校验结果"):
#         allure.attach(str(left), left_name)
#         allure.attach(str(right), right_name)
#     return pytest_output
