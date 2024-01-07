from abc import *


class UserUseCase(metaclass=ABCMeta):
    @abstractmethod
    def check_exist_user(self, field, value) -> bool:
        pass
