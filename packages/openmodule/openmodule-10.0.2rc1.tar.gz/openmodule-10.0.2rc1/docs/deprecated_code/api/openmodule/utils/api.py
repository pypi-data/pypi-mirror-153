import logging
from enum import Enum

import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth


class ApiException(Exception):
    def __init__(self, status_code, msg="", response=None):
        if status_code in [503, 412, 500, 408]:
            retry = True
        else:
            retry = False
        self.status = status_code
        self.msg = msg
        self.retry = retry
        self.response = response

    def __str__(self):
        return f"Api Error {self.status}: {self.msg}"


class AuthMethod(str, Enum):
    digest = "digest"
    basic = "basic"
    none = "none"
    header = "header"


class Api:
    """
    Api template class
    provides basic request functionality
    """

    def __init__(self, host, auth_type: AuthMethod, verify_ssl: bool, user: str = "user", password: str = "password",
                 timeout=10, *args, **kwargs):
        self.server_host = host
        self.auth = self.get_auth(auth_type, user, password)
        self.verify_ssl = verify_ssl
        self.request_timeout = timeout

    @classmethod
    def get_auth(cls, auth_type, user, password):
        if auth_type == AuthMethod.basic:
            return HTTPBasicAuth(user, password)
        elif auth_type == AuthMethod.digest:
            return HTTPDigestAuth(user, password)
        elif auth_type == AuthMethod.header:
            return {user: password}
        else:
            return None

    @classmethod
    def _common_headers(cls):
        return {}

    def _request(self, method, url, payload=None, json_response=True, **kwargs):
        url = f"{self.server_host.rstrip('/')}/{url}"
        timeout = kwargs.pop("timeout", self.request_timeout)
        headers = self._common_headers()
        headers.update(kwargs.pop("headers", {}))
        result = None
        try:
            logging.debug(f"Sending {method} request to {url}")
            if isinstance(self.auth, (HTTPBasicAuth, HTTPDigestAuth)):
                kwargs["auth"] = self.auth
            elif isinstance(self.auth, dict):
                headers.update(self.auth)

            result = requests.request(method.upper(), url, **kwargs, timeout=timeout, headers=headers,
                                      verify=self.verify_ssl, json=payload)
            if 200 <= result.status_code < 300:
                if json_response:
                    return result.json()
                return result.content
        except requests.Timeout:
            raise ApiException(status_code=408, msg=f"Timeout after {timeout}s")
        except Exception as e:
            raise ApiException(status_code=400, msg=str(e), response=result)
        raise ApiException(status_code=result.status_code, msg="Server error", response=result)

    def get(self, url, payload=None, json_response=True, **kwargs):
        return self._request("GET", url, payload, json_response, **kwargs)

    def post(self, url, payload=None, json_response=True, **kwargs):
        return self._request("POST", url, payload, json_response, **kwargs)

    def put(self, url, payload=None, json_response=True, **kwargs):
        return self._request("PUT", url, payload, json_response, **kwargs)

    def delete(self, url, payload=None, json_response=True, **kwargs):
        return self._request("DELETE", url, payload, json_response, **kwargs)
