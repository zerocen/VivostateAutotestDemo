from api_test.api.vivostate_api import VivostateApi


class OrganizationApi(VivostateApi):

    def create_organization(self, parent_id, name, active, available, description):
        path = "/admin/api/organizations"
        data = {
            "parentId": parent_id,
            "active": active,
            "available": available,
            "description": description,
            "name": name,
            "type": "ORGANIZATION"
        }
        response = self.send_request("POST", self.base_url + path, json=data)
        return response.status_code, response.json() if response.text else None

    def get_organization_by_id(self, organization_id):
        path = f"/admin/api/organizations/{organization_id}"
        response = self.send_request("GET", self.base_url + path)
        return response.status_code, response.json() if response.text else None

    def update_organization(self, organization_id, name, description, active, available):
        path = f"/admin/api/organizations/{organization_id}"
        data = {
            "name": name,
            "description": description,
            "active": active,
            "available": available
        }
        response = self.send_request("PUT", self.base_url + path, json=data)
        return response.status_code, response.json() if response.text else None

    def search_organization(self, filter, page_number, rows_per_page):
        path = f"/admin/api/organizations/search"
        params = {
            "filter": filter,
            "pageNumber": page_number,
            "rowsPerPage": rows_per_page
        }
        response = self.send_request("GET", self.base_url + path, params=params)
        return response.status_code, response.json() if response.text else None

    def delete_organization(self, organization_id):
        path = f"/admin/api/organizations/{organization_id}"
        response = self.send_request("DELETE", self.base_url + path)
        return response.status_code, response.json() if response.text else None
