from api_test.api.vivostate_api import VivostateApi


class TerminalApi(VivostateApi):

    def create_terminal(self, parent_id, name, description, serial_number):
        path = "/admin/api/terminals"
        data = {
            "name": name,
            "description": description,
            "parentId": parent_id,
            "type": "TERMINAL",
            "active": True,
            "available": True,
            "serialNumber": serial_number,
            "model": {
                "id": 16,
                "name": "VP6800",
                "partNumber": "IDV68-*",
                "manufacturer": {
                    "id": 2,
                    "name": "ID TECH",
                    "website": "https://idtechproducts.com"
                }
            },
            "timeZone": "UTC",
            "lastContact": "1980-01-01T00:00:00",
            "nextContact": "1980-01-01T00:00:00",
            "lastDownload": "1980-01-01T00:00:00",
            "heartbeat": True,
            "directiveForceAppUpdate": False,
            "directiveReboot": False,
            "frequency": 300,
            "debugExpirationDate": "1980-01-01T00:00:00",
            "debugActive": False,
            "syncClock": False
        }
        response = self.send_request("POST", self.base_url + path, json=data)
        return response.status_code, response.json()

    def delete_terminal(self, terminal_id):
        path = f"/admin/api/terminals/{terminal_id}"
        response = self.send_request("DELETE", self.base_url + path)
        return response.status_code, response.json()
