from .defualt import DefaultException


class DomainException(DefaultException):
    def __init__(self, msg):
        super().__init__(msg=msg)


class InvalidState(DomainException):
    def __init__(self, msg='유효하지 않은 상태 코드'):
        super().__init__(msg=msg)


class ParticipationFailed(DomainException):
    def __init__(self, msg='참여 실패'):
        super().__init__(msg=msg)


class LeaveFailed(DomainException):
    def __init__(self, msg='탈퇴 실패'):
        super().__init__(msg=msg)


class VerifyFail(DomainException):
    def __init__(self, msg='검증 실패'):
        super().__init__(msg=msg)
