from abc import *


class ProfileQueryUseCase(metaclass=ABCMeta):
    def get(self, user_id):
        pass


class ProfileDeleteUseCase(metaclass=ABCMeta):
    def delete(self, user_id):
        pass


class ProfileUpdateUseCase(metaclass=ABCMeta):
    def update_password(self, user_id, current_password, new_password):
        pass

    def update_nickname(self, user_id, nickname):
        pass

    def update_account_number(self, user_id, account_number):
        pass
