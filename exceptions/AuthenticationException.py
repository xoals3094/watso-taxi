from .DefaultException import DefaultException


class AuthenticationException(DefaultException):
    def __init__(self, msg, code):
        super().__init__(msg=msg, code=code)


class AccessDeniedException(AuthenticationException):
    def __init__(self, msg='권한이 없습니다', code=100):
        super().__init__(msg=msg, code=code)


class SigninFailedException(AuthenticationException):
    def __init__(self, msg='아이디 혹은 비밀번호가 일치하지 않습니다', code=101):
        super().__init__(msg=msg, code=code)