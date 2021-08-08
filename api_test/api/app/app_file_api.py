from api_test.api.vivostate_api import VivostateApi


class AppFileApi(VivostateApi):

    def upload_file_to_app(self, app_id, description, file_path):
        path = f"/tms/api/apps/{app_id}"
        file = {
            "file": open(file_path, "rb")
        }
        params = {
            "description": description
        }
        self.session.headers.pop("Content-Type")
        response = self.send_request("POST", self.base_url + path, files=file, params=params)
        self.session.headers["Content-Type"] = "application/json; charset=utf-8"
        return response.status_code, response.json()
