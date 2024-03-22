from enum import Enum
from exceptions import DomainException


class Status(str, Enum):
    RECRUITING = 'RECRUITING'
    CLOSED = 'CLOSED'
    BOARDING = 'BOARDING'
    SETTLEMENT = 'SETTLEMENT'
    COMPLETED = 'COMPLETED'

    def modify(self):
        if self not in [Status.RECRUITING, Status.CLOSED]:
            raise DomainException.PostModificationFailedException(
                msg=f"'{self}' 상태에서는 게시글의 수정이 불가능합니다."
            )

    def to(self, status):
        if (self is Status.RECRUITING) and (status in [Status.RECRUITING, Status.CLOSED]):
            return

        elif (self is Status.CLOSED) and (status in [Status.RECRUITING, Status.CLOSED, Status.BOARDING]):
            return

        elif (self is Status.BOARDING) and (status is Status.SETTLEMENT):
            return

        elif (self is Status.SETTLEMENT) and (status is Status.COMPLETED):
            return

        raise DomainException.InvalidStateException(
            msg=f"'{self}' -> '{status}'는 허용되지 않는 상태코드 변경입니다."
        )

    def participate(self):
        if self != Status.RECRUITING:
            raise DomainException.ParticipationFailedException(
                msg=f"'{self}' 상태에서는 참여가 불가능합니다."
            )

    def leave(self):
        if self != Status.RECRUITING:
            raise DomainException.LeaveFailedException(
                msg=f"'{self}' 상태에서는 탈퇴가 불가능합니다."
            )

