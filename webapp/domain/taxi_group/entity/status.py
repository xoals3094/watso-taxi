from enum import Enum
from webapp.common.exceptions import domain


class Status(str, Enum):
    OPEN = 'OPEN'
    CLOSE = 'CLOSE'
    SETTLE = 'SETTLE'
    COMPLETE = 'COMPLETE'

    def to(self, status):
        if (self is Status.OPEN) and (status in [Status.OPEN, Status.CLOSE]):
            return

        elif (self is Status.CLOSE) and (status in [Status.OPEN, Status.CLOSE, Status.SETTLE]):
            return

        elif (self is Status.SETTLE) and (status is Status.COMPLETE):
            return

        raise domain.InvalidState(
            msg=f"'{self}' -> '{status}'는 허용되지 않는 상태코드 변경입니다."
        )
