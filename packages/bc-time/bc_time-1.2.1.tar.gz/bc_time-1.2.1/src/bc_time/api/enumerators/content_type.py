from enum import unique, IntEnum

@unique
class ContentType(IntEnum):
    user = 10
    device = 18
    employee = 22
    branch = 35
    employee_leave = 50
    settings = 86
    employee_overtime_rule_detail = 103
    employee_group_membership = 105
    department = 39
    visitor = 95
    visitor_group = 99
    security_details = 250
    security_area_duration = 252 # How much time spent in area(s).
    visitor_security_details = 350
    visitor_security_area_duration = 352 # How much time spent in area(s).
    controller = 111
    company_profile_user_membership = 114
    company_profile_user_membership_email_confirm = 115
    visitor_group_membership = 116
    visitor_group_area_membership = 117
    current_company_profile = 118