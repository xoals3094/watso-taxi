from domain.auth.persistance.token_dao import MySQLTokenDao
from domain.auth.exception import persistence
from util.token_decoder import decode_token
from util.token_generator import create_access_token, create_refresh_token

from exceptions import auth


class JWTLoginService:
    def __init__(self, token_dao: MySQLTokenDao):
        self.token_dao = token_dao

    def refresh(self, refresh_token) -> (str, str):
        try:
            user_id = self.token_dao.find_user_id_by_refresh_token(refresh_token)
        except persistence.ResourceNotFound:
            raise auth.LoginFail(msg='로그인 정보가 없습니다')

        access_token = create_access_token(user_id)

        try:
            decode_token(refresh_token)
        except auth.TokenExpired:
            refresh_token = create_refresh_token()
            self.token_dao.update_both(user_id, access_token, refresh_token)
        else:
            self.token_dao.update_access_token(user_id, access_token)

        return access_token, refresh_token



