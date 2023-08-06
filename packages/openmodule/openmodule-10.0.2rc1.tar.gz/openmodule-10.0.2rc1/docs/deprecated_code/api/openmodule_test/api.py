import requests
import requests_mock

from openmodule_test.utils import DeveloperError


class ApiMocker:
    host = None

    def __init__(self, mocker):
        self.mocker = mocker
        if not self.host:
            raise DeveloperError("you need to set a host")

    def server_url(self, url):
        return f"{self.host.rstrip('/')}/{url}"

    def ok(self):
        self.mocker.get(requests_mock.ANY, status_code=200, json={})
        self.mocker.post(requests_mock.ANY, status_code=200, json={})
        self.mocker.put(requests_mock.ANY, status_code=200, json={})
        self.mocker.delete(requests_mock.ANY, status_code=200, json={})

    def timeout(self):
        self.mocker.get(requests_mock.ANY, exc=requests.exceptions.ConnectTimeout)
        self.mocker.post(requests_mock.ANY, exc=requests.exceptions.ConnectTimeout)
        self.mocker.put(requests_mock.ANY, exc=requests.exceptions.ConnectTimeout)
        self.mocker.delete(requests_mock.ANY, exc=requests.exceptions.ConnectTimeout)

    def unavailable(self):
        self.mocker.get(requests_mock.ANY, status_code=503, json={})
        self.mocker.post(requests_mock.ANY, status_code=503, json={})
        self.mocker.put(requests_mock.ANY, status_code=503, json={})
        self.mocker.delete(requests_mock.ANY, status_code=503, json={})

    def server_error(self):
        self.mocker.get(requests_mock.ANY, status_code=500, json={})
        self.mocker.post(requests_mock.ANY, status_code=500, json={})
        self.mocker.put(requests_mock.ANY, status_code=500, json={})
        self.mocker.delete(requests_mock.ANY, status_code=500, json={})

    def invalid_auth(self):
        self.mocker.get(requests_mock.ANY, status_code=403, json={})
        self.mocker.post(requests_mock.ANY, status_code=403, json={})
        self.mocker.get(requests_mock.ANY, status_code=403, json={})
        self.mocker.post(requests_mock.ANY, status_code=403, json={})

    def bad_request(self):
        self.mocker.get(requests_mock.ANY, status_code=400, json={})
        self.mocker.post(requests_mock.ANY, status_code=400, json={})
        self.mocker.get(requests_mock.ANY, status_code=400, json={})
        self.mocker.post(requests_mock.ANY, status_code=400, json={})

    def not_found(self):
        self.mocker.get(requests_mock.ANY, status_code=404, json={})
        self.mocker.post(requests_mock.ANY, status_code=404, json={})
        self.mocker.get(requests_mock.ANY, status_code=404, json={})
        self.mocker.post(requests_mock.ANY, status_code=404, json={})
