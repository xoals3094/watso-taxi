from webapp.domain.auth.persistance.user_dao import MySQLUserDao
from webapp.domain.auth.persistance.token_dao import MySQLTokenDao
from webapp.domain.auth.persistance.kakao_dao import get_user_info
from webapp.domain.auth.exception import persistence
from webapp.common.util.token_generator import create_access_token, create_refresh_token


class KakaoLoginService:
    def __init__(self, user_dao: MySQLUserDao, token_dao: MySQLTokenDao):
        self.user_dao = user_dao
        self.token_dao = token_dao

    def login(self, access_token) -> (str, str):
        kakao_user_info = get_user_info(access_token)

        try:
            user_id = self.user_dao.find_id_by_kakao_id(kakao_user_info.id)
        except persistence.ResourceNotFound:
            user_id = self.user_dao.create(kakao_user_info.id, kakao_user_info.nickname, kakao_user_info.profile_image_url)

        access_token = create_access_token(user_id)
        refresh_token = create_refresh_token()

        self.token_dao.insert(user_id, access_token, refresh_token)

        return access_token, refresh_token

