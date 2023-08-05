import json
import requests
from requests import Response
from requests_facade.config import FERNET_KEY
from generic_utils import CleanDevGenericUtils
from requests_facade.config import _auth_payload
from requests_facade.config import _endpoint_auth
from requests_facade.config import _properties_auth
from requests_facade.config import _properties_endpoint_config

utils: CleanDevGenericUtils = CleanDevGenericUtils()

default_header: dict = {
    'Content-type': 'application/json',
    'accept': 'application/json'
}

class RequestFacade:
    need_auth: bool
    __token: str = ''

    def __init__(self, need_auth: bool = False):
        self.need_auth = need_auth
        self._jwt_token()

    @property
    def __header(self) -> dict:
        if self.need_auth:
            jwt_key: dict = {'Authorization': f'Bearer {self.__token}'}
            header = default_header | jwt_key
            return header
        else:
            return default_header

    def _jwt_token(self) -> str:
        if self.__token:
            return self.__token
        url: str = f"{_properties_endpoint_config['url_api']}{_endpoint_auth}"
        resp: Response = requests.post(url=f'{url}', json=_auth_payload, headers=self.__header)
        self.__token = json.loads(resp.text)['token']

    def get(self, url):
        resp: Response = requests.get(url=url, headers=self.__header, auth=False)
        return resp

    def post(self, url: str, data: dict):
        return requests.post(url=f'{url}', headers=self.__header, data=json.dumps(data))

