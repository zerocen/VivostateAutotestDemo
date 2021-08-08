import os
import pytest
import allure
from utils.data_loader import DataLoader
from utils.data_path_manager import data_path_manager


@allure.severity(allure.severity_level.BLOCKER)
@allure.feature("Personalization Test")
class TestPersonalization:
    test_data_path = os.path.join(f"{data_path_manager.page_data_dir}",
                                  "personalization", "personalization_page_params.yml")
    organization_test_data = DataLoader.load_test_case_data(test_data_path)

    create_organization_data = organization_test_data["create_organization"]["data"]
    create_organization_ids = organization_test_data["create_organization"]["ids"]

    delete_organization_data = organization_test_data["delete_organization"]["data"]
    delete_organization_ids = organization_test_data["delete_organization"]["ids"]

    edit_organization_data = organization_test_data["edit_organization"]["data"]
    edit_organization_ids = organization_test_data["edit_organization"]["ids"]

    @allure.story("Add organization entity")
    @allure.title("Add organization entity")
    @pytest.mark.parametrize("entity_type, name, description",
                             create_organization_data, ids=create_organization_ids)
    def test_add_organization_entity(self, app, entity_type, name, description):
        with allure.step("Go to personalization page"):
            personalization_page = app.go_to_personalization_page()

        with allure.step("Create organization"):
            personalization_page.select_root_entity().add_entity(entity_type, name, description)

        with allure.step("Check result"):
            details = personalization_page.get_selected_entity_details()
            created_entity_type = details["type"]
            created_entity_name = details["name"]
            created_entity_description = details["description"]

            assert entity_type == created_entity_type and name == created_entity_name and \
                   description == created_entity_description, \
                   "The information of the organization is not as expected."

    @allure.story("Edit organization entity")
    @allure.title("Edit organization entity")
    @pytest.mark.parametrize("old_name, new_name, new_description",
                             edit_organization_data, ids=edit_organization_ids)
    def test_edit_organization_entity(self, app, old_name, new_name, new_description):

        with allure.step("Go to personalization page"):
            personalization_page = app.go_to_personalization_page()

        with allure.step("edit organization click save"):
            personalization_page.open_entity_by_search(old_name).edit_entity(new_name, new_description)

        with allure.step("Check result"):
            details = personalization_page.get_selected_entity_details()
            edited_name = details["name"]
            edited_description = details["description"]

            assert new_name == edited_name and new_description == edited_description, \
                "The information of the edited entity is not as expected."

    @allure.story("Delete organization entity")
    @allure.title("Delete organization entity")
    @pytest.mark.parametrize("name",
                             delete_organization_data, ids=delete_organization_ids)
    def test_delete_organization_entity(self, app, name):
        with allure.step("Go to personalization page"):
            personalization_page = app.go_to_personalization_page()

        with allure.step("Delete entity"):
            personalization_page.open_entity_by_search(name).delete_entity()

        with allure.step("Check result"):
            assert not personalization_page.can_entity_be_found(name)
