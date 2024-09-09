from .defualt import DefaultException


class AuthenticationException(DefaultException):
    def __init__(self, msg):
        super().__init__(msg=msg)


class AccessDenied(AuthenticationException):
    def __init__(self, msg='권한이 없습니다'):
        super().__init__(msg=msg)


class LoginFail(AuthenticationException):
    def __init__(self, msg):
        super().__init__(msg=msg)


class TokenExpired(AuthenticationException):
    def __init__(self, msg):
        super().__init__(msg=msg)
