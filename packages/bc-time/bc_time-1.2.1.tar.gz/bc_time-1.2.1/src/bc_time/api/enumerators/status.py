from enum import unique, IntEnum

@unique
class Status(IntEnum):
    active = 1
    inactive = 2