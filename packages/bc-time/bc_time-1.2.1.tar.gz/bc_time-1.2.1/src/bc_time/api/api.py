from os.path import exists as path_exists
from pathlib import Path
from json import dumps as json_dumps
from requests import post as requests_post, get as requests_get, codes as requests_status_codes
from configparser import ConfigParser
from bc_time.system.encryption.crypt import Crypt
from bc_time.system.validate import Validate
from bc_time.requests.base import Base as RequestsBase
from bc_time.oauth2.constants.grant_type import GrantType as OAuth2GrantType
from bc_time.oauth2.token import Token
from bc_time.api.constants.api import Api as ApiConstants
from bc_time.api.enumerators.content_type import ContentType

class Api(RequestsBase):
    client_id = None
    client_secret = None
    crypt_key = None
    grant_type = None
    code = None

    __crypt = None
    __token = None

    @property
    def crypt(self) -> Crypt:
        if not self.__crypt:
            self.__crypt = Crypt(key=self.crypt_key)
        return self.__crypt

    @property
    def token(self):
        if not self.__token:
            self.__token = Token(
                client_id=self.client_id,
                client_secret=self.client_secret,
                crypt_key=self.crypt_key,
                grant_type=self.grant_type,
                code=self.code
            )
        return self.__token

    def __init__(self, grant_type: str=None, code: str=None) -> None:
        self.__init_authentication_credentials_from_file()
        if grant_type:
            self.grant_type = grant_type
        if code:
            self.code = code
        self.token.crypt = self.crypt

    def __init_authentication_credentials_from_file(self, file_path: str='.bc_time/credentials', section: str='default'):
        time_config_file_path = f"{str(Path.home())}/{file_path}"
        if not path_exists(time_config_file_path):
            return
        config_parser = ConfigParser(inline_comment_prefixes=';')
        config_parser.read(time_config_file_path)
        if section not in config_parser:
            return
        config_data_keys_and_attributes = ['client_id', 'client_secret', 'crypt_key', 'grant_type']
        for config_data_key_or_attribute in config_data_keys_and_attributes:
            if config_data_key_or_attribute in config_parser[section]:
                setattr(
                    self,
                    config_data_key_or_attribute,
                    config_parser[section][config_data_key_or_attribute]
                )

    def create(self, content_type_id: ContentType, payload: dict, content_uid: int=None) -> dict:
        request_token_result, request_token_response_data = self.token.request_token()
        if not request_token_result:
            return request_token_response_data
        create_payload = self.__get_create_or_update_data(
            content_type_id=content_type_id,
            payload=payload,
            content_uid=content_uid
        )
        post_response = requests_post(
            url=ApiConstants.API_URL,
            data=create_payload
        )
        return self._get_response_data(post_response.text) if post_response.status_code == requests_status_codes.ok else None

    def update(self, content_type_id: ContentType, content_uid: int, payload: dict) -> dict:
        request_token_result, request_token_response_data = self.token.request_token()
        if not request_token_result:
            return request_token_response_data
        update_payload = self.__get_create_or_update_data(
            content_type_id,
            content_uid=content_uid,
            payload=payload
        )
        post_response = requests_post(
            url=ApiConstants.API_URL,
            data=update_payload
        )
        return self._get_response_data(post_response.text) if post_response.status_code == requests_status_codes.ok else None

    def __get_create_or_update_data(self, content_type_id: ContentType, payload: dict, content_uid: int=None) -> dict:
        data = {'content_type_id' : int(content_type_id)}
        if content_uid: # Will be omitted if performing POST (1 new object).
            data['content_uid'] = content_uid
        if payload:
            if content_uid != ApiConstants.UID_POST_MANY:
                data.update(payload)
            else:
                data['data'] = payload
        create_or_update_payload = {'access_token' : self.token.token}
        if self.crypt_key:
            self.crypt.data = json_dumps(data)
            create_or_update_payload['data'] = self.crypt.encrypt()
        else:
            create_or_update_payload.update(data)
        return create_or_update_payload

    def get_all_using_pagination(self, content_type_id: ContentType, content_uid: int=ApiConstants.UID_GET_ALL, filters: dict=None, page: int=1, row_count: int=ApiConstants.DEFAULT_ROW_COUNT) -> dict:
        if not self.token.request_token():
            return None
        request_params = self.__get_request_params(
            content_type_id=content_type_id,
            content_uids=[content_uid],
            filters=filters,
            page=page,
            row_count=row_count
        )
        request_response = requests_get(
            url=ApiConstants.API_URL,
            params=request_params
        )
        return self._get_response_data(request_response.text) if request_response.status_code == requests_status_codes.ok else None

    def get_one(self, content_type_id: ContentType, content_uid: int) -> dict:
        if not self.token.request_token():
            return None
        request_params = self.__get_request_params(content_type_id, content_uids=[content_uid])
        request_response = requests_get(
            url=ApiConstants.API_URL,
            params=request_params
        )
        return self._get_response_data(request_response.text) if request_response.status_code == requests_status_codes.ok else None

    def get_many(self, content_type_id: ContentType, content_uids: list) -> dict:
        if not self.token.request_token():
            return None
        request_params = self.__get_request_params(content_type_id, content_uids)
        request_response = requests_get(
            url=ApiConstants.API_URL,
            params=request_params
        )
        return self._get_response_data(request_response.text) if request_response.status_code == requests_status_codes.ok else None

    def __get_request_params(self, content_type_id: ContentType, content_uids: list=None, filters: dict=None, page: int=None, row_count: int=None) -> dict:
        data = {
            'content_type_id' : int(content_type_id),
            'content_uid' : content_uids[0] if len(content_uids) == 1 else ','.join([str(content_uid) for content_uid in content_uids]),
        }
        if self.__can_paginate(page, row_count):
            data['page'] = page
            data['row_count'] = row_count
        if filters:
            data.update(filters)
        request_params = {'access_token' : self.token.token}
        if self.crypt_key:
            self.crypt.data = json_dumps(data)
            request_params['data'] = self.crypt.encrypt()
        else:
            request_params.update(data)
        return request_params

    def __can_paginate(self, page: int, row_count: int) -> bool:
        if not Validate.is_numeric(page, min=1):
            return False
        return Validate.is_numeric(row_count, min=1, max=ApiConstants.DEFAULT_ROW_COUNT)