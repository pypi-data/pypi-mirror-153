class Api:
    OAUTH2_TOKEN_URL = 'https://time-v2.bcity.me/oauth2/token/'
    OAUTH2_AUTHORISE_URL = 'https://time-v2.bcity.me/oauth2/authorise/'
    API_URL = 'https://time-v2.bcity.me/api/'
    DEFAULT_ROW_COUNT = 100 # 100 is the maximum no. of rows the API allows to retrieved at a time.
    UID_GET_ALL = -1
    UID_POST_MANY = -2