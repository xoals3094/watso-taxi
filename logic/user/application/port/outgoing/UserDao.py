from abc import *


class UserDao(metaclass=ABCMeta):
    @abstractmethod
    def is_already_exist_username(self, username) -> bool:
        pass

    @abstractmethod
    def is_already_exist_nickname(self, nickname) -> bool:
        pass

    @abstractmethod
    def is_already_exist_email(self, email) -> bool:
        pass

    @abstractmethod
    def update_pw(self, user_id, pw):
        pass

    @abstractmethod
    def update_email(self, user_id, email):
        pass

    @abstractmethod
    def update_nickname(self, user_id, nickname):
        pass

    @abstractmethod
    def update_account_number(self, user_id, account_number):
        pass
