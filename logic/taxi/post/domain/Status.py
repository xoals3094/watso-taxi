from enum import Enum


class Status(str, Enum):
    RECRUITING = 'RECRUITING'
    CLOSE = 'CLOSED'
    BOARDING = 'BOARDING'
    SETTLE = 'SETTLE'
    COMPLETION = 'COMPLETION'
