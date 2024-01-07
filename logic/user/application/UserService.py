from logic.user.application.port.incoming.UserUseCase import UserUseCase
from logic.user.application.port.outgoing.UserDao import UserDao


class UserService(UserUseCase):
    def __init__(self, user_dao: UserDao):
        self.user_dao = user_dao

    def check_exist_user(self, field, value) -> bool:
        if field == 'username':
            return self.user_dao.is_already_exist_username(value)

        elif field == 'nickname':
            return self.user_dao.is_already_exist_nickname(value)

        elif field == 'email':
            return self.user_dao.is_already_exist_email(value)
