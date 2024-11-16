from webapp.common.exceptions import auth, persistence
from webapp.common.util.token_decoder import get_token_id_and_exp
from webapp.domain.auth.entity.token import Token
from webapp.domain.auth.persistance.token_repository import TokenRepository


class JWTAuthService:
    def __init__(self, token_repository: TokenRepository, ):
        self.token_repository = token_repository

    def login(self, user_id: str) -> (str, str):
        token = Token.create(user_id)
        self.token_repository.save(token)
        return (
            token.access_token,
            token.refresh_token
        )

    def logout(self, refresh_token):
        token_id, exp = get_token_id_and_exp(refresh_token)
        self.token_repository.delete(token_id)

    def refresh(self, refresh_token, fcm_token) -> (str, str):
        token_id, exp = get_token_id_and_exp(refresh_token)

        try:
            token = self.token_repository.find_by_id(token_id)
        except persistence.ResourceNotFound:
            raise auth.LoginFail(msg='로그인 정보가 없습니다')

        token.refresh(exp)
        token.user.device.fcm_token = fcm_token
        self.token_repository.save(token)

        return (
            token.access_token,
            token.refresh_token
        )
