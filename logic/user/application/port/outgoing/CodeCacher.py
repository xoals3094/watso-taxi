from abc import *


class CodeCacher(metaclass=ABCMeta):
    @abstractmethod
    def get_code_by_email(self, email) -> str:
        pass

    @abstractmethod
    def save(self, email, code):
        pass

    @abstractmethod
    def delete(self, email):
        pass
