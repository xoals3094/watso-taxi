import exceptions
from flask import current_app
import jwt
import time
from datetime import datetime, timedelta
from logic.user.application.port.incoming.AuthUseCase import AuthUseCase
from logic.user.application.port.outgoing.UserRepository import UserRepository
from logic.user.application.port.outgoing.TokenDao import TokenDao


class JwtAuthService(AuthUseCase):
    def __init__(self, user_repository: UserRepository, token_dao: TokenDao):
        self.user_repository = user_repository
        self.token_dao = token_dao

    def login(self, username, pw):
        try:
            user = self.user_repository.find_user_by_username(username)
        except exceptions.NotExistResource:
            raise exceptions.SigninFail

        if user.compare_pw(pw) is False:
            raise exceptions.SigninFail

        access_token = self._create_access_token(user._id, user.nickname, current_app.secret_key)
        refresh_token = self._create_refresh_token(current_app.secret_key)
        self.token_dao.save(user._id, access_token, refresh_token)

        return access_token, refresh_token

    def logout(self, access_token):
        self.token_dao.delete(access_token)

    def refresh(self, refresh_token) -> str:
        try:
            token = self.token_dao.find_token_by_refresh_token(refresh_token)
        except exceptions.NotExistResource:
            raise exceptions.NotExistToken

        user = token['user']
        access_token = self._create_access_token(user['_id'], user['nickname'], current_app.secret_key)
        self.token_dao.update_access_token(user['_id'], access_token)
        return access_token

    @staticmethod
    def _create_access_token(user_id, nickname, secret_key):
        payload = {
            'user_id': user_id,
            'nickname': nickname,
            'exp': datetime.utcnow() + timedelta(minutes=30)
        }

        return jwt.encode(payload, secret_key)

    @staticmethod
    def _create_refresh_token(secret_key):
        payload = {
            'exp': datetime.utcnow() + timedelta(days=90)
        }
        return jwt.encode(payload, secret_key)
