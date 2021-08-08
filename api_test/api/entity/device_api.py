from api_test.api.vivostate_api import VivostateApi


class DeviceApi(VivostateApi):

    def create_device(self, parent_id, name, description, serial_number):
        path = "/admin/api/devices"
        data = {
            "name": name,
            "description": description,
            "parentId": parent_id,
            "type": "DEVICE",
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
            "lastContact": "1980-01-01T00:00:00",
            "nextContact": "1980-01-01T00:00:00",
            "lastDownload": "1980-01-01T00:00:00"
        }
        response = self.send_request("POST", self.base_url + path, json=data)
        return response.status_code, response.json()

    def delete_device(self, device_id):
        path = f"/admin/api/devices/{device_id}"
        response = self.send_request("POST", self.base_url + path)
        return response.status_code, response.json()
