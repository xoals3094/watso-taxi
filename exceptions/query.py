from .defualt import DefaultException


class QueryException(DefaultException):
    def __init__(self, msg):
        super().__init__(msg=msg)


class ResourceNotFound(QueryException):
    def __init__(self, msg):
        super().__init__(msg=msg)
