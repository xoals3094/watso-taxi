from logic.auth.application.port.outgoing.KakaoDao import KakaoDao
from logic.auth.application.port.outgoing.UserDao import UserDao
from datetime import datetime, timedelta
from config.production.setting import secret_key
import jwt


class KakaoLoginService:
    def __init__(self, kakao_dao: KakaoDao, user_dao: UserDao):
        self.kakao_dao = kakao_dao
        self.user_dao = user_dao

    def login(self, authorization_code) -> (str, str):
        access_token, refresh_token = self.kakao_dao.get_token(authorization_code)
        kakao_user_info = self.kakao_dao.get_user_info(access_token, refresh_token)

        user = self.user_dao.find_user_by_kakao_id(kakao_user_info.id)
        if user is None:
            user = self.user_dao.create(kakao_user_info.nickname, kakao_user_info.profile_image_url, kakao_user_info.id)

        access_token = self._create_access_token(user.id, secret_key)
        refresh_token = self._create_refresh_token(secret_key)

        return access_token, refresh_token

    @staticmethod
    def _create_access_token(id, secret_key):
        payload = {
            'id': str(id),
            'exp': datetime.utcnow() + timedelta(minutes=30)
        }
        return jwt.encode(payload, secret_key)

    @staticmethod
    def _create_refresh_token(secret_key):
        payload = {
            'exp': datetime.utcnow() + timedelta(days=90)
        }
        return jwt.encode(payload, secret_key)
