import json

import requests

from severino.settings import SEVERINO_API_TOKEN


class Http:
    def __init__(self):
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Token {SEVERINO_API_TOKEN}",
        }

    def __http_request(
        self, method: str, url: str, headers: dict = None, data=None, params=None
    ):
        if headers is None:
            headers = {}

        if data is None:
            data = {}

        headers = {**self.headers, **headers}
        return requests.request(
            method=method,
            url=url,
            headers=headers,
            data=json.dumps(data),
            params=params,
        )

    def post(self, url: str, headers: dict = None, data: dict = None):
        return self.__http_request(method="POST", url=url, headers=headers, data=data)

    def get(
        self, url: str, headers: dict = None, data: dict = None, params: dict = None
    ):
        return self.__http_request(
            method="GET", url=url, headers=headers, data=data, params=params
        )

    def put(self, url: str, headers: dict = None, data: dict = None):
        return self.__http_request(method="PUT", url=url, headers=headers, data=data)

    def patch(self, url: str, headers: dict = None, data: dict = None):
        return self.__http_request(method="PATCH", url=url, headers=headers, data=data)

    def delete(self, url: str, headers: dict = None, data: dict = None):
        return self.__http_request(method="DELETE", url=url, headers=headers, data=data)
