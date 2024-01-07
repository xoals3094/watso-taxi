from enum import Enum


class Status(str, Enum):
    RECRUITING = 'RECRUITING'
    CLOSE = 'CLOSE'
    BOARDING = 'BOARDING'
    SETTLE = 'SETTLE'
    COMPLETION = 'COMPLETION'
