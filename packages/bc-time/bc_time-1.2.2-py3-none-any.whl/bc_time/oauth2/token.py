from datetime import datetime, timezone, timedelta
from requests import post as requests_post, codes as requests_status_codes
from bc_time.requests.base import Base as RequestsBase
from bc_time.oauth2.constants.grant_type import GrantType as OAuth2GrantType
from bc_time.api.constants.api import Api as ApiConstants
from bc_time.system.encryption.crypt import Crypt
from bc_time.system.constants.datetime.format import Format as DateTimeFormat

class Token(RequestsBase):
    grant_type = None
    client_id = None
    client_secret = None
    code = None
    crypt_key = None
    private_key_file_path = None
    token = None
    token_expire_as_str = None # This will be stored in UTC.

    __crypt = None

    @property
    def crypt(self) -> Crypt:
        if not self.__crypt:
            self.__crypt = Crypt(key=self.crypt_key)
        return self.__crypt

    @crypt.setter
    def crypt(self, value: Crypt):
        self.__crypt = value

    def __init__(self, client_id: str=None, client_secret: str=None, crypt_key: str=None, grant_type: str=None, code: str=None) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.crypt_key = crypt_key
        self.grant_type = grant_type
        self.code = code

    def request_token(self) -> tuple[bool, dict]:
        if self.__has_valid_token():
            return True, None
        if not self.__validate_data():
            return False, None
        data = self.__get_data()
        if not data:
            return False, None
        request_response = requests_post(
            url=ApiConstants.OAUTH2_TOKEN_URL,
            data=data
        )
        if request_response.status_code != requests_status_codes.ok:
            return False, None
        response_data = self._get_response_data(request_response.text)
        if not set(('access_token', 'expires_in')).issubset(response_data.keys()):
            return False, response_data
        self.token = response_data['access_token']
        token_expire = datetime.now(timezone.utc) + timedelta(seconds=response_data['expires_in'])
        self.token_expire_as_str = token_expire.strftime(DateTimeFormat.MY_SQL_DATE_TIME)
        return True, response_data

    def __has_valid_token(self) -> bool:
        if not self.token or not self.token_expire_as_str:
            return False
        now = datetime.now(timezone.utc)
        return self.token_expire_as_str > now.strftime(DateTimeFormat.MY_SQL_DATE_TIME)

    def __validate_data(self) -> bool:
        if self.grant_type == OAuth2GrantType.AUTH_CODE:
            return self.client_id and self.client_secret and self.code
        elif self.grant_type == OAuth2GrantType.CLIENT_CREDENTIALS:
            return self.client_id and self.client_secret
        elif self.grant_type == OAuth2GrantType.JWT_BEARER:
            return self.client_id and self.private_key_file_path
        return False

    def __get_data(self) -> str:
        if self.grant_type == OAuth2GrantType.AUTH_CODE:
            return {
                'grant_type' : self.grant_type,
                'client_id' : self.client_id,
                'client_secret' : self.__get_client_secret(),
                'code' : self.code,
            }
        elif self.grant_type == OAuth2GrantType.CLIENT_CREDENTIALS:
            return {
                'grant_type' : self.grant_type,
                'client_id' : self.client_id,
                'client_secret' : self.__get_client_secret(),
            }
        elif self.grant_type == OAuth2GrantType.JWT_BEARER:
            return None
        return None

    def __get_client_secret(self):
        if self.crypt_key:
            self.crypt.data = self.client_secret
            return self.crypt.encrypt()
        return self.client_secret