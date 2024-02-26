from enum import Enum


class Status(str, Enum):
    RECRUITING = 'RECRUITING'
    CLOSED = 'CLOSED'
    BOARDING = 'BOARDING'
    SETTLEMENT = 'SETTLEMENT'
    COMPLETED = 'COMPLETED'

    def modifiable(self):
        if self in [Status.RECRUITING, Status.CLOSED]:
            return True
        return False

    def changeable(self, status):
        if self is Status.RECRUITING:
            return status in [Status.RECRUITING, Status.CLOSED]

        elif self is Status.CLOSED:
            return status in [Status.RECRUITING, Status.CLOSED, Status.BOARDING]

        elif self is Status.BOARDING:
            return status is Status.SETTLEMENT

        elif self is Status.SETTLEMENT:
            return status is Status.COMPLETED

    def can_participate(self):
        return self == Status.RECRUITING

    def can_leave(self):
        return self == Status.RECRUITING
