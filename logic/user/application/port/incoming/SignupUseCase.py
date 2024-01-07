from abc import *
from logic.user.dto.presentaition import SignupModel


class SignupAuthUseCase(metaclass=ABCMeta):
    @abstractmethod
    def send_auth_email(self, email):
        pass

    @abstractmethod
    def validate_auth_code(self, email, auth_code):
        pass


class SignupUseCase(metaclass=ABCMeta):
    @abstractmethod
    def signup(self, signup_model: SignupModel):
        pass
