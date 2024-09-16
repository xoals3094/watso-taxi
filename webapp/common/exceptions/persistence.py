from .defualt import DefaultException


class ResourceNotFound(DefaultException):
    def __init__(self, msg='리소스를 찾을 수 없습니다'):
        super(ResourceNotFound, self).__init__(msg=msg)
