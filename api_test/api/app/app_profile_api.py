from api_test.api.vivostate_api import VivostateApi


class AppProfileApi(VivostateApi):

    def add_profile_to_app(self, app_id, name, active):
        path = f"/tms/api/apps/{app_id}/appprofile"
        data = {
            "active": active,
            "name": name
        }
        response = self.send_request("POST", self.base_url + path, json=data)
        return response.status_code, response.json()
