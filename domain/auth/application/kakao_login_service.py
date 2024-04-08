from domain.auth.persistance.user_dao import MongoDBUserDao
from domain.auth.util.token_generator import TokenGenerator


class KakaoLoginService:
    def __init__(self, kakao_dao, user_dao: MongoDBUserDao):
        self.kakao_dao = kakao_dao
        self.user_dao = user_dao

    def login(self, access_token) -> (str, str):
        kakao_user_info = self.kakao_dao.get_user_info(access_token)
        user_id = self.user_dao.find_id_by_kakao_id(kakao_user_info.id)
        if user_id is None:
            user_id = self.user_dao.create(kakao_user_info.nickname, kakao_user_info.profile_image_url, kakao_user_info.id)

        access_token = TokenGenerator.create_access_token(user_id)
        refresh_token = TokenGenerator.create_refresh_token()

        return access_token, refresh_token

