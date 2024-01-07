from abc import *


class MessagePusher(metaclass=ABCMeta):
    @abstractmethod
    def send(self, data, tokens):
        pass
