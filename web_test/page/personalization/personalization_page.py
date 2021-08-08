import os
from selenium.common.exceptions import NoSuchElementException
from utils.data_path_manager import data_path_manager
from web_test.page.base_page import BasePage
from utils.logger import logger


class PersonalizationPage(BasePage):
    page_function_file = os.path.join(data_path_manager.page_data_dir, "personalization",
                                      "personalization_page_functions.yml")

    def open_entity_by_search(self, entity_name=""):
        params = {
            "entity_name": entity_name
        }
        logger.info(f"Open entity by searching entity name. Params={params}")
        self.perform_functions(self.page_function_file, "open_entity_by_search", params)
        return self

    def select_root_entity(self):
        logger.info("select root entity")
        self.perform_functions(self.page_function_file, "select_root_entity")
        return self

    def get_entity_keyword_display(self, entity_name):
        params = {
            "entity_name": entity_name,
            "entity_keyword_display": "entity_keyword"
        }
        logger.info(f"Get entity keyword display. Params={params}")
        info = self.perform_functions(self.page_function_file, "get_entity_keyword_display", params)
        logger.info(f"entity  keyword display: {info[params['entity_keyword_display']]}")
        return info[params["entity_keyword_display"]]

    def click_the_pop_of_select_any_entity_to_select_package(self):
        logger.info("click x of select any entity to select package")
        self.perform_functions(self.page_function_file, "click_the_pop_of_select_any_entity_to_select_package")
        return self

    def can_entity_be_found(self, entity_name):
        params = {
            "entity_name": entity_name
        }
        logger.info(f"Search entity. Params={params}")
        try:
            self.perform_functions(self.page_function_file, "open_entity_by_search", params)
        except NoSuchElementException:
            return False
        else:
            return True

    def add_entity(self, entity_type, entity_name, description, model=None, serial_number=None, schedule=None):
        params = {
            "entity_type": entity_type,
            "entity_name": entity_name,
            "description": description,
            "model": model,
            "serial_number": serial_number,
            "schedule": schedule
        }
        logger.info(f"Add entity. Params={params}")
        self.perform_functions(self.page_function_file, "add_entity", params)
        return self

    def edit_entity(self, entity_name, entity_description, available=None):
        params = {
            "entity_name": entity_name,
            "description": entity_description,
            "available": available
        }
        logger.info(f"Edit entity. Params={params}")
        self.perform_functions(self.page_function_file, "edit_entity", params)
        return self

    def delete_entity(self):
        logger.info("delete entity")
        self.perform_functions(self.page_function_file, "delete_entity")
        return self

    def get_selected_entity_name_and_serial(self):
        params = {
            "name_key": "name",
            "serial_key": "serial"
        }
        logger.info("Get the name and serial of selected entity.")
        info = self.perform_functions(self.page_function_file, "get_selected_entity_name_and_serial", params)
        info["name"] = info["name"][2:]
        logger.info(f"Entity info: {info}")
        return info

    def get_selected_entity_details(self):
        params = {
            "type_key": "type",
            "name_key": "name",
            "id_key": "id",
            "description_key": "description",
            "entity_number_key": "entity_number",
            "entity_key_key": "entity_key",
            "model_key": "model",
            "serial_key": "serial",
            "available_key": "available",
            "force_update_key": "force_update",
            "force_reboot_key": "force_reboot",
            "frequency_key": "frequency",
            "schedule_key": "schedule"
        }
        logger.info("Get the details of entity.")
        info = self.perform_functions(self.page_function_file, "get_selected_entity_details", params)
        info[params["force_update_key"]] = "true" if info[params["force_update_key"]] else "false"
        info[params["force_reboot_key"]] = "true" if info[params["force_reboot_key"]] else "false"
        logger.info(f"Entity details: {info}")
        return info

    def get_notification_caption(self):
        params = {
            "notification_key": "notification"
        }
        logger.info("Get the notification caption.")
        info = self.perform_functions(self.page_function_file, "get_notification_caption", params)
        logger.info(f"notification caption: {info}")
        return info[params["notification_key"]]
