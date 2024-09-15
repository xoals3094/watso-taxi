from webapp.common.exceptions import auth, persistence
from webapp.common.util.token_decoder import get_token_id_and_exp
from webapp.domain.auth.entity.token import Token
from webapp.domain.auth.entity.kakao import Kakao
from webapp.domain.auth.persistance.kakao_repository import KakaoRepository
from webapp.domain.auth.persistance.token_repository import TokenRepository
from webapp.domain.auth.third_party import kakao_login_client


class AuthService:
    def __init__(
            self,
            kakao_repository: KakaoRepository,
            token_repository: TokenRepository
    ):
        self.kakao_repository = kakao_repository
        self.token_repository = token_repository

    def login(self, access_token) -> (str, str):
        kakao_user_info = kakao_login_client.get_user_info(access_token)
        try:
            kakao = self.kakao_repository.find_by_id(kakao_id=kakao_user_info.id)
            user_id = kakao.id
        except persistence.ResourceNotFound:
            kakao = Kakao.create(
                kakao_id=kakao_user_info.id,
                nickname=kakao_user_info.nickname,
                profile_image_url=kakao_user_info.profile_image_url
            )
            user_id = kakao.id
            self.kakao_repository.save(kakao)

        token = Token.create(user_id)
        self.token_repository.save(token)

        return (
            token.access_token,
            token.refresh_token
        )

    def logout(self, refresh_token):
        token_id, exp = get_token_id_and_exp(refresh_token)
        self.token_repository.delete(token_id)

    def refresh(self, refresh_token) -> (str, str):
        token_id, exp = get_token_id_and_exp(refresh_token)

        try:
            token = self.token_repository.find_by_id(token_id)
        except persistence.ResourceNotFound:
            raise auth.LoginFail(msg='로그인 정보가 없습니다')

        token.refresh(exp)
        self.token_repository.save(token)

        return (
            token.access_token,
            token.refresh_token
        )
