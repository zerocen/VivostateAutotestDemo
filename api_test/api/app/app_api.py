from api_test.api.vivostate_api import VivostateApi


class AppApi(VivostateApi):

    def create_app(self, owner_id, name, description, model_id, version, available):
        path = "/tms/api/apps/createApp"
        data = {
            "available": available,
            "description": description,
            "modelId": model_id,
            "name": name,
            "ownerId": owner_id,
            "version": version
        }
        response = self.send_request("POST", self.base_url + path, json=data)
        return response.status_code, response.json()

    def delete_app(self, app_id):
        path = f"/tms/api/apps/{app_id}"
        response = self.send_request("DELETE", self.base_url + path)
        return response.status_code, response.json()
