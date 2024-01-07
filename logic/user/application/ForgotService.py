import exceptions

from logic.user.application.port.outgoing.UserRepository import UserRepository
from logic.user.application.port.outgoing.UserDao import UserDao
from logic.user.application.port.incoming.ForgotUseCase import ForgotUsernameUseCase, ForgotPasswordUseCase
from logic.user.util.TempPasswordGenerator import generate_temp_password
from logic.user.util.PasswordHashing import pw_hashing

from blinker import signal

forgot_signal = signal('forgot-signal')


class ForgotUsernameService(ForgotUsernameUseCase):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def send_username_email(self, email):
        try:
            user = self.user_repository.find_user_by_email(email)
        except exceptions.NotExistResource:
            raise exceptions.NotExistUser

        forgot_signal.send('username', email=email, username=user.username)


class ForgotPasswordService(ForgotPasswordUseCase):
    def __init__(self, user_repository: UserRepository, user_dao: UserDao):
        self.user_repository = user_repository
        self.user_dao = user_dao

    def send_temp_password(self, username, email):
        try:
            user = self.user_repository.find_user_by_username(username)
        except exceptions.NotExistResource:
            raise exceptions.NotExistUser

        if user.email != email:
            raise exceptions.NotExistUser

        temp_password = generate_temp_password()
        user.pw = pw_hashing(temp_password)

        self.user_dao.update_pw(user._id, user.pw)
        forgot_signal.send('temp-password', temp_password=temp_password, email=email)
