from enum import Enum
from exceptions import domain


class Status(str, Enum):
    RECRUITING = 'RECRUITING'
    CLOSED = 'CLOSED'
    SETTLEMENT = 'SETTLEMENT'
    COMPLETED = 'COMPLETED'

    def to(self, status):
        if (self is Status.RECRUITING) and (status in [Status.RECRUITING, Status.CLOSED]):
            return

        elif (self is Status.CLOSED) and (status in [Status.RECRUITING, Status.CLOSED, Status.SETTLEMENT]):
            return

        elif (self is Status.SETTLEMENT) and (status is Status.COMPLETED):
            return

        raise domain.InvalidState(
            msg=f"'{self}' -> '{status}'는 허용되지 않는 상태코드 변경입니다."
        )
