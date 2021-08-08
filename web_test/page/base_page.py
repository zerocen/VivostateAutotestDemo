import inspect
import re
from time import sleep, time
from functools import wraps
import allure
import yaml
from selenium.common.exceptions import ElementClickInterceptedException, ElementNotInteractableException, \
    TimeoutException, StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from utils.configurator import config
from utils.logger import logger


class BasePage:
    execute_in_batch = False

    def __init__(self, driver: WebDriver = None):
        self.driver = driver

    def handle_stale_element(timeout):
        def decorator(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                end_time = time() + timeout
                while time() < end_time:
                    try:
                        return func(self, *args, **kwargs)
                    except StaleElementReferenceException:
                        pass
            return wrapper
        return decorator

    def find(self, locator):
        return self.driver.find_element(*locator)

    def finds(self, locator):
        return self.driver.find_elements(*locator)

    def wait(self, timeout, condition, message=""):
        WebDriverWait(self.driver, timeout).until(condition, message)

    @handle_stale_element(5)
    def click_element(self, locator):
        element = self.find(locator)
        try:
            element.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", element)
        except ElementNotInteractableException:
            self.driver.execute_script("arguments[0].scrollIntoView(false);", element)
            WebDriverWait(self.driver, 5).until(ec.element_to_be_clickable(locator)).click()

    @handle_stale_element(5)
    def context_click(self, locator):
        element = self.find(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(false);", element)
        ActionChains(self.driver).context_click(element).perform()

    def click_perform(self, locator):
        element = self.find(locator)
        ActionChains(self.driver).click(element).perform()

    def input_text(self, locator, text):
        element = self.find(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(false);", element)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        if self.execute_in_batch:
            text_list = []
            elements = self.finds(locator)
            for element in elements:
                text_list.append(element.text)
            return text_list
        return self.find(locator).text

    def check_element_visibility(self, locator):
        elements = self.finds(locator)
        return len(elements) > 0

    def get_attribute(self, locator, element_attribute):
        if self.execute_in_batch:
            attribute_list = []
            elements = self.finds(locator)
            for element in elements:
                attribute_list.append(element.get_attribute(element_attribute))
            return attribute_list
        return self.find(locator).get_attribute(element_attribute)

    def wait_for_element_visible(self, locator, timeout=5):
        self.driver.implicitly_wait(0.5)
        wait_condition = ec.visibility_of_element_located(locator)
        try:
            self.wait(timeout, wait_condition, f"Element {locator} is still invisible")
        except TimeoutException as e:
            raise e
        finally:
            self.driver.implicitly_wait(config["driver_config"]["default_implicit_waiting_time"])

    def wait_for_element_invisible(self, locator, timeout=5):
        self.driver.implicitly_wait(0.5)
        elements = self.finds(locator)
        if len(elements) > 0:
            wait_condition = ec.invisibility_of_element_located(locator)
            try:
                self.wait(timeout, wait_condition, f"Element {locator} is still visible")
            except TimeoutException as e:
                raise e
            finally:
                self.driver.implicitly_wait(config["driver_config"]["default_implicit_waiting_time"])
        self.driver.implicitly_wait(config["driver_config"]["default_implicit_waiting_time"])

    def wait_for_text_to_be_element_attribute(self, locator, element_attribute, text, timeout=5):
        def wait_condition(driver):
            try:
                attribute_value = driver.find_element(*locator).get_attribute(element_attribute)
                return attribute_value == text
            except StaleElementReferenceException:
                return False

        self.driver.implicitly_wait(0.5)
        try:
            self.wait(timeout, wait_condition, f"Element attribute [{element_attribute}] is not equal to {text}")
        except TimeoutException as e:
            raise e
        finally:
            self.driver.implicitly_wait(config["driver_config"]["default_implicit_waiting_time"])

    def capture_screenshot(self):
        logger.debug("Capturing screenshot...")
        return self.driver.get_screenshot_as_png()

    def execute_script(self, locator, script):
        element = None
        if locator:
            element = self.find(locator)
        return self.driver.execute_script(script, element)

    def handle_alert(self, alert_type, action, text=None):
        alert: Alert = WebDriverWait(self.driver, 5).until(ec.alert_is_present())
        alert_text = alert.text
        if alert_type != "alert" and alert_type != "confirm" and alert_type != "prompt":
            raise ValueError(f"Unsupported alert type: [{alert_type}]")

        if text and alert_type == "prompt":
            alert.send_keys(text)

        if action == "accept":
            alert.accept()
        elif action == "dismiss":
            alert.dismiss()
        else:
            raise ValueError(f"The alert type [{alert_type}] doesn't support the action [{action}]")
        return alert_text

    def execute_command(self, command: str, locator: tuple, params: dict):
        if command == "pause":
            sleep(params["time"])
            return None
        else:
            func = eval(f"self.{command}")
            func_args = list(inspect.signature(func).parameters.keys())
            func_params = {}
            for key in func_args:
                if key == "locator":
                    func_params[key] = locator
                elif key in params:
                    func_params[key] = params[key]
            return func(**func_params)

    def perform_functions(self, function_file, function_name, params=None):
        if params is None:
            params = {}

        response = {}
        pattern = re.compile(r"{(.+?)}")
        keys_check_variable = ["element", "elements", "text", "store_key", "enabled", "script"]

        logger.debug(f"Perform function: {function_name}")
        with open(function_file, "r", encoding="utf-8") as f:
            functions = yaml.safe_load(f)
        steps = functions[function_name]

        for step in steps:
            logger.debug(f"Execute command [{step['command']}], details: {step}")

            # Replace the placeholder with the params value
            for key in keys_check_variable:
                if key in step:
                    tmp_str = str(step[key])
                    matches = pattern.findall(tmp_str)
                    for match in matches:
                        value = "" if params[match] is None else params[match]
                        tmp_str = tmp_str.replace(f"{{{match}}}", value)
                    else:
                        step[key] = tmp_str

            with allure.step(step["step_id"]):
                # Check if the step is enabled
                if "enabled" in step and (
                        isinstance(step["enabled"], str) and (step["enabled"] == "false" or not step["enabled"]) or
                        isinstance(step["enabled"], bool) and not step["enabled"]
                ):
                    logger.debug(f"Skip step [{step['step_id']}]")
                    continue

                # Parse element locator
                # supported locator strategies: id, xpath, link text, partial link text, name, tag name, class name,
                # css selector
                locator = None
                if "element" in step:
                    locator = step["element"].split("=", 1)
                if "elements" in step:
                    locator = step["elements"].split("=", 1)
                if locator:
                    locator[0] = locator[0].replace("_", " ")

                # Execute command
                try:
                    # if step["command"] == "click_element":
                    #     self.click_element(locator)
                    # elif step["command"] == "context_click":
                    #     self.context_click(locator)
                    # elif step["command"] == "input_text":
                    #     self.input_text(locator, step["text"])
                    # elif step["command"] == "get_text":
                    #     response[step["store_key"]] = self.get_text(locator)
                    # elif step["command"] == "get_attribute":
                    #     response[step["store_key"]] = self.get_attribute(locator, step["element_attribute"])
                    # elif step["command"] == "wait_for_element_visible":
                    #     self.wait_for_element_visible(locator, step["timeout"])
                    # elif step["command"] == "wait_for_element_invisible":
                    #     self.wait_for_element_invisible(locator, step["timeout"])
                    # elif step["command"] == "pause":
                    #     sleep(step["time"])
                    if "elements" in step:
                        self.execute_in_batch = True
                    else:
                        self.execute_in_batch = False
                    return_value = self.execute_command(step["command"], locator, step)
                    if "store_key" in step:
                        response[step["store_key"]] = return_value
                except Exception as e:
                    logger.error(f"Execute command [{step['command']}] error", exc_info=True)
                    allure.attach(
                        self.capture_screenshot(), "Exception picture", attachment_type=allure.attachment_type.PNG)
                    raise e

        return response
