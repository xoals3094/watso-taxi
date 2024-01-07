from abc import *


class AuthUseCase(metaclass=ABCMeta):
    @abstractmethod
    def login(self, username, pw):
        pass

    @abstractmethod
    def logout(self, key):
        pass
