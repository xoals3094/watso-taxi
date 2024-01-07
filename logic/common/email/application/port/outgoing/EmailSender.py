from abc import *


class EmailSender(metaclass=ABCMeta):
    @abstractmethod
    def send(self, to, subject, body):
        pass
