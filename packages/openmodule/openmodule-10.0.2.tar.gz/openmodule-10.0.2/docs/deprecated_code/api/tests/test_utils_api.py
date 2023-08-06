import base64
from unittest import TestCase

import requests
import requests_mock

from openmodule.utils.api import Api
from openmodule.utils.api import ApiException, AuthMethod
from openmodule_test.api import ApiMocker


class Mocker(ApiMocker):
    host = "http://asdf"

    def test_bad(self):
        self.mocker.get(self.server_url("abc/"), status_code=400)

    def bad_json(self):
        self.mocker.get(self.server_url("abc/"), status_code=200)

    def sleep(self):
        self.mocker.get(self.server_url("abc/"), exc=requests.exceptions.ConnectTimeout)


class ApiExceptionTestCase(TestCase):
    def test(self):
        retry_status = [503, 408, 500, 412]
        other = [400, 404, 300, 403]
        for status in retry_status:
            e = ApiException(status_code=status)
            self.assertEqual(True, e.retry)
        for status in other:
            e = ApiException(status_code=status)
            self.assertEqual(False, e.retry)


class ApiTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.api = Api("http://asdf", AuthMethod("none"), False, timeout=1)
        cls.api1 = Api("http://asdf", AuthMethod("basic"), False, timeout=1)
        cls.api2 = Api("http://asdf", AuthMethod("digest"), False, timeout=1)

    @requests_mock.Mocker(real_http=False)
    def test_header_authorization(self, m: requests_mock.Mocker):
        mocker = Mocker(m)
        mocker.ok()

        api = Api("http://asdf", AuthMethod("header"), verify_ssl=False)
        api.get("abc/")

        self.assertEqual("password", m.request_history[0].headers.get("user"))

    @requests_mock.Mocker(real_http=False)
    def test_basic_authorization(self, m: requests_mock.Mocker):
        mocker = Mocker(m)
        mocker.ok()

        api = Api("http://asdf", AuthMethod("basic"), verify_ssl=False)
        api.get("abc/")

        self.assertEqual(f"Basic {base64.b64encode(b'user:password').decode()}",
                         m.request_history[0].headers.get("Authorization"))

    @requests_mock.Mocker(real_http=False)
    def test_methods_ok(self, m):
        api = Mocker(m)
        api.ok()

        self.api.get("abc/")
        self.api.post("abc/")
        self.api.put("abc/")
        self.api.delete("abc/")

    @requests_mock.Mocker(real_http=False)
    def test_methods_bad(self, m):
        api = Mocker(m)
        api.test_bad()
        with self.assertRaises(ApiException) as e:
            self.api.get("abc/")
        self.assertEqual(400, e.exception.status)
        self.assertIn("400", str(e.exception))

        api.timeout()
        with self.assertRaises(ApiException) as e:
            self.api.get("abc/")
        self.assertEqual(408, e.exception.status)
        self.assertIn("408", str(e.exception))

        api.bad_json()
        with self.assertRaises(ApiException) as e:
            self.api.get("abc/")
        self.assertEqual(400, e.exception.status)
        self.assertIn("400", str(e.exception))

        self.api.get("abc/", json_response=False)
