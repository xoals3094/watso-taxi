from abc import *


class ForgotUsernameUseCase(metaclass=ABCMeta):
    @abstractmethod
    def send_username_email(self, email):
        pass


class ForgotPasswordUseCase(metaclass=ABCMeta):
    @abstractmethod
    def send_temp_password(self, username, email):
        pass
    