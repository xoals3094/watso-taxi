from logic.user.application.port.incoming.ProfileUseCase import ProfileQueryUseCase, ProfileDeleteUseCase, ProfileUpdateUseCase
from logic.user.application.port.outgoing.UserRepository import UserRepository
from logic.user.application.port.outgoing.UserDao import UserDao
from logic.user.util.PasswordHashing import pw_hashing
import exceptions


class ProfileQueryService(ProfileQueryUseCase):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def get(self, user_id):
        try:
            user = self.user_repository.find_user_by_id(user_id)
        except exceptions.NotExistResource:
            raise exceptions.NotExistUser

        return user


class ProfileDeleteService(ProfileDeleteUseCase):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def delete(self, user_id):
        self.user_repository.delete(user_id)


class ProfileUpdateService(ProfileUpdateUseCase):
    def __init__(self, user_repository: UserRepository, user_dao: UserDao):
        self.user_repository = user_repository
        self.user_dao = user_dao

    def update_password(self, user_id, current_password, new_password):
        try:
            user = self.user_repository.find_user_by_id(user_id)
        except exceptions.NotExistResource:
            raise exceptions.NotExistUser

        if user.compare_pw(current_password) is False:
            raise exceptions.PasswordMismatch

        hashed_pw = pw_hashing(new_password)
        self.user_dao.update_pw(user_id, hashed_pw)

    def update_nickname(self, user_id, nickname):
        self.user_dao.update_nickname(user_id, nickname)

    def update_account_number(self, user_id, account_number):
        self.user_dao.update_account_number(user_id, account_number)
