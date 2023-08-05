from enum import unique, IntEnum

@unique
class RequestStatus(IntEnum):
    none = 0
    success = 1
    data_invalid = 2
    insufficient_access = 3
    error = 4
    client_id_invalid = 5
    client_secret_invalid = 6
    method_invalid = 7
    content_type_id_invalid = 8
    uid_invalid = 9
    field_invalid = 10
    user_uid_invalid = 11
    post_batch_data_invalid = 12
    data_empty = 13
    no_response = 14 # No internet connection, blocked by firewall, etc.; used exclusively by Time Comm.
    response_invalid = 15 # Http code is anything other than 200 (OK); used exclusively by Time Comm.
    response_json_invalid = 16 # Used exclusively by Time Comm.
    company_profile_inactive = 17
    cost_plan_overdue = 18
    token_invalid = 19
    token_expired = 20
    authentication_credentials_invalid = 21 # Raised by Time Comm. Service.