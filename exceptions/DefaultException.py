class DefaultException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

    @property
    def json(self):
        return {
            'msg': self.msg
        }
