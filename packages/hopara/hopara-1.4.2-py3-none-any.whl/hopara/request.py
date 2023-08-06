import json

import requests
from requests.compat import urljoin
import logging


class Request:
    def __init__(self, config: object, header: dict = None):
        self.config = config
        self.__access_token = None
        self.__header = header if header else {}

    def __get_headers(self) -> dict:
        self.__header['Authorization'] = 'Bearer ' + self.get_access_token()
        return self.__header

    def get_access_token(self) -> str:
        if self.__access_token:
            return self.__access_token
        url = urljoin(self.config.get_auth_url(), 'token')
        response = requests.post(url, json=self.config.get_credentials())
        response.raise_for_status()
        self.__access_token = response.json()['access_token']
        return self.__access_token

    @staticmethod
    def __handle_response(response: requests.Response, ignore_404: bool = False) -> requests.Response:
        if response.status_code == 200 or (ignore_404 and response.status_code == 404):
            return response
        if response.headers.get('Content-Type') == 'application/json':
            logging.info(json.dumps(response.json(), indent=True))
        else:
            logging.info(response.content)
        response.reason = response.content
        response.raise_for_status()

    def post(self, url: str, body: dict) -> requests.Response:
        return self.__handle_response(requests.post(url, json=body, headers=self.__get_headers()))

    def get(self, url: str, body: dict) -> requests.Response:
        return self.__handle_response(requests.get(url, json=body, headers=self.__get_headers()))

    def delete(self, url: str, body: dict) -> requests.Response:
        return self.__handle_response(requests.delete(url, json=body, headers=self.__get_headers()), ignore_404=True)
