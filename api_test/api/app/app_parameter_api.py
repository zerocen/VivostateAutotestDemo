from api_test.api.vivostate_api import VivostateApi


class AppParameterApi(VivostateApi):

    def add_parameter_to_app(self, app_id, name, description):
        path = f"/tms/api/apps/{app_id}/appparam"
        data = {
            "name": name,
            "description": description,
            "appParamFormat": {
                "id": 3,
                "name": "boolean",
                "value": "boolean"
            },
            "action": {
                "id": 1,
                "name": "Action1"
            }
        }
        response = self.send_request("POST", self.base_url + path, json=data)
        return response.status_code, response.json()
