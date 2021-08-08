from api_test.api.vivostate_api import VivostateApi


class MerchantApi(VivostateApi):

    def create_merchant(self, parent_id, name, description):
        path = "/admin/api/merchants"
        data = {
            "parentId": parent_id,
            "active": True,
            "available": True,
            "description": description,
            "name": name,
            "type": "MERCHANT"
        }
        response = self.send_request("POST", self.base_url + path, json=data)
        return response.status_code, response.json()

    def delete_merchant(self, merchant_id):
        path = f"/admin/api/merchants/{merchant_id}"
        response = self.send_request("DELETE", self.base_url + path)
        return response.status_code, response.json()
