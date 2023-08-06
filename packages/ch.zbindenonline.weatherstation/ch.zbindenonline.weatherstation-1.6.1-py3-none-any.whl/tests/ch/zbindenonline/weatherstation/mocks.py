import json

from requests.models import HTTPError


class ResponseContent:
    def __init__(self, json_data):
        self.json_data = json_data

    def decode(self, utf):
        if self.json_data is None:
            return None
        return json.dumps(self.json_data)


class MockResponse:
    def __init__(self, json_data=None, status_code=200, error_info: str = None):
        self.status_code = status_code
        self.ok = 200 == status_code
        self.content = ResponseContent(json_data)
        self.error_info = error_info

    def raise_for_status(self):
        raise HTTPError()
