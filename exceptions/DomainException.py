from .DefaultException import DefaultException


class DomainException(DefaultException):
    def __init__(self, msg):
        super().__init__(msg=msg)


class PostModificationFailedException(DomainException):
    def __init__(self, msg):
        super().__init__(msg=msg)


class InvalidStateException(DomainException):
    def __init__(self, msg):
        super().__init__(msg=msg)


class ParticipationFailedException(DomainException):
    def __init__(self, msg):
        super().__init__(msg=msg)


class LeaveFailedException(DomainException):
    def __init__(self, msg):
        super().__init__(msg=msg)
