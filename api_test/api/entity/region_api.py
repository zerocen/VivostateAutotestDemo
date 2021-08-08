from api_test.api.vivostate_api import VivostateApi


class RegionApi(VivostateApi):

    def create_region(self, parent_id, name, description):
        path = "/admin/api/regions"
        data = {
            "parentId": parent_id,
            "active": True,
            "available": True,
            "description": description,
            "name": name,
            "type": "REGION"
        }
        response = self.send_request("POST", self.base_url + path, json=data)
        return response.status_code, response.json()

    def delete_region(self, region_id):
        path = f"/admin/api/regions/{region_id}"
        response = self.send_request("DELETE", self.base_url + path)
        return response.status_code, response.json()
