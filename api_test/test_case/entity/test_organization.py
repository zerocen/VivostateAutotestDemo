import os.path
import allure
import pytest
from utils.data_loader import DataLoader
from utils.data_path_manager import data_path_manager


@allure.severity(allure.severity_level.BLOCKER)
@allure.feature("Organization Management Test")
class TestOrganization:
    test_data_path = os.path.join(f"{data_path_manager.api_data_dir}", "entity", "organization_params.yml")
    organization_test_data = DataLoader.load_test_case_data(test_data_path)

    create_organization_test_data = organization_test_data["create_organization"]["data"]
    create_organization_test_ids = organization_test_data["create_organization"]["ids"]

    get_organization_test_data = organization_test_data["get_organization_by_id"]["data"]
    get_organization_test_ids = organization_test_data["get_organization_by_id"]["ids"]

    update_organization_test_data = organization_test_data["update_organization"]["data"]
    update_organization_test_ids = organization_test_data["update_organization"]["ids"]

    search_organization_test_data = organization_test_data["search_organization"]["data"]
    search_organization_test_ids = organization_test_data["search_organization"]["ids"]

    delete_organization_test_data = organization_test_data["delete_organization"]["data"]
    delete_organization_test_ids = organization_test_data["delete_organization"]["ids"]

    @allure.story("Create organization")
    @allure.title("Create organization")
    @pytest.mark.parametrize("parent_id, name, active, available, description, http_code, api_code",
                             create_organization_test_data, ids=create_organization_test_ids)
    def test_create_organization(self, organization, parent_id, name, active, available, description,
                                 http_code, api_code):
        with allure.step("Create organization"):
            create_status_code, create_res = organization.create_organization(
                parent_id, name, active, available, description)
            is_code_correct = (create_res and
                               (api_code == create_res["code"] if api_code else "code" not in create_res))
            assert create_status_code == http_code and is_code_correct

        with allure.step("Check created organization info"):
            if create_status_code // 100 == 2 and "code" not in create_res:
                assert parent_id == create_res["parentId"] and name == create_res["name"] and \
                       active == create_res["active"] and available == create_res["available"] and \
                       description == create_res["description"], "Creating organization failed!"

                organization_id = create_res["entityId"]
                get_status_code, get_res = organization.get_organization_by_id(organization_id)
                assert get_status_code == 200 and "code" not in get_res and \
                       parent_id == get_res["parentId"] and organization_id == get_res["entityId"] and \
                       name == get_res["name"] and active == get_res["active"] and \
                       available == get_res["available"] and description == get_res["description"], \
                       "The created organization information does not match expectations"

    @allure.story("Get organization information")
    @allure.title("Get organization information")
    @pytest.mark.parametrize("organization_id, parent_id, name, active, available, description, "
                             "http_code, api_code", get_organization_test_data, ids=get_organization_test_ids)
    def test_get_organization_by_id(self, organization, organization_id, parent_id, name, active, available,
                                    description, http_code, api_code):
        with allure.step("Create organization"):
            if not organization_id:
                create_status_code, create_res = organization.create_organization(
                    parent_id, name, active, available, description)
                assert create_status_code == 201 and "code" not in create_res, "Creating organization failed!"
                organization_id = create_res["entityId"]

        with allure.step("Get organization info"):
            get_status_code, get_res = organization.get_organization_by_id(organization_id)
            is_code_correct = (get_res and (api_code == get_res["code"] if api_code else "code" not in get_res))
            assert get_status_code == http_code and is_code_correct

            if get_status_code // 100 == 2 and "code" not in get_res and parent_id:
                assert organization_id == get_res["entityId"] and parent_id == get_res["parentId"] and \
                       name == get_res["name"] and active == get_res["active"] and \
                       available == get_res["available"] and description == get_res["description"]

    @allure.story("Update organization information")
    @allure.title("Update organization information")
    @pytest.mark.parametrize("organization_id, parent_id, name, active, available, description, new_name, new_active, "
                             "new_available, new_description, http_code, api_code",
                             update_organization_test_data, ids=update_organization_test_ids)
    def test_update_organization(self, organization, organization_id, parent_id, name, active, available, description,
                                 new_name, new_active, new_available, new_description, http_code, api_code):
        with allure.step("Create organization"):
            if not organization_id:
                create_status_code, create_res = organization.create_organization(
                    parent_id, name, active, available, description)
                assert create_status_code == 201 and "code" not in create_res, "Creating organization failed."
                organization_id = create_res["entityId"]

        with allure.step("Update organization"):
            update_status_code, update_res = organization.update_organization(
                organization_id, new_name, new_description, new_active, new_available)
            is_code_correct = (update_res and
                               (api_code == update_res["code"] if api_code else "code" not in update_res))
            assert update_status_code == http_code and is_code_correct

            is_updated = update_status_code // 100 == 2 and "code" not in update_res and parent_id
            if is_updated:
                assert update_res["name"] == new_name and update_res["description"] == new_description and \
                       update_res["active"] == new_active and update_res["available"] == new_available, \
                       "Updating organization information failed."

        with allure.step("Check updated organization info"):
            if update_status_code != 404:
                get_status_code, get_res = organization.get_organization_by_id(organization_id)
                if is_updated:
                    assert get_status_code == 200 and "code" not in get_res and \
                           get_res["name"] == new_name and get_res["description"] == new_description and \
                           get_res["active"] == new_active and get_res["available"] == new_available, \
                           "The updated organization information does not match expectations."
                else:
                    assert get_status_code == 200 and "code" not in get_res and \
                           get_res["name"] == name and get_res["description"] == description and \
                           get_res["active"] == active and get_res["available"] == available, \
                           "The organization information was changed when the updating failed."

    @allure.story("Search organization")
    @allure.title("Search organization")
    @pytest.mark.parametrize("parent_id, name, active, available, description, filter_string, "
                             "page_number, rows_per_page, http_code",
                             search_organization_test_data, ids=search_organization_test_ids)
    def test_search_organization(self, organization, parent_id, name, active, available, description,
                                 filter_string, page_number, rows_per_page, http_code):
        with allure.step("Create organization"):
            create_status_code, create_res = organization.create_organization(
                parent_id, name, active, available, description)
            assert create_status_code == 201 and "code" not in create_res
            organization_id = create_res["entityId"]

        search_status_code, search_res = organization.search_organization(filter_string, page_number, rows_per_page)
        filter_list = list(filter(lambda x: x["entityId"] == organization_id and x["parentId"] == parent_id and
                                  x["name"] == name and x["active"] == active and x["available"] == available and
                                  x["description"] == description, search_res))

        assert search_status_code == http_code and len(filter_list) == 1

    @allure.story("Delete organization")
    @allure.title("Delete organization")
    @pytest.mark.parametrize("organization_id, parent_id, name, active, available, description, "
                             "http_status_code, code", delete_organization_test_data, ids=delete_organization_test_ids)
    def test_delete_organization(self, organization, organization_id, parent_id, name, active, available, description,
                                 http_status_code, code):
        with allure.step("Create organization"):
            if not organization_id:
                create_status_code, create_res = organization.create_organization(
                    parent_id, name, active, available, description)
                assert create_status_code == 201 and "code" not in create_res, "Creating organization failed."
                organization_id = create_res["entityId"]

        with allure.step("Delete organization"):
            delete_status_code, delete_res = organization.delete_organization(organization_id)
            is_code_correct = (not delete_res or (code == delete_res["code"] if code else not delete_res))
            assert delete_status_code == http_status_code and is_code_correct

        with allure.step("Check the deleted organization info"):
            if delete_status_code != 404:
                get_status_code, get_res = organization.get_organization_by_id(organization_id)
                assert get_status_code == 200 and "code" not in get_res and \
                       organization_id == get_res["entityId"] and not get_res["active"]
