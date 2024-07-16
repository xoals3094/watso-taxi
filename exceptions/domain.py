from .defualt import DefaultException


class DomainException(DefaultException):
    def __init__(self, msg):
        super().__init__(msg=msg)


class InvalidState(DomainException):
    def __init__(self, msg):
        super().__init__(msg=msg)


class ParticipationFailed(DomainException):
    def __init__(self, msg):
        super().__init__(msg=msg)


class LeaveFailed(DomainException):
    def __init__(self, msg):
        super().__init__(msg=msg)


class VerifyFail(DomainException):
    def __init__(self, msg):
        super().__init__(msg=msg)
