from datetime import datetime, timedelta
from webapp.common.schmea.models import User, Kakao, Token
from webapp.common.exceptions import auth, persistence
from webapp.common.util.token_decoder import get_token_id_and_exp
from webapp.common.util.token_generator import create_access_token, create_refresh_token
from webapp.domain.auth.persistance.kakao_repository import KakaoRepository
from webapp.domain.auth.persistance.user_repository import UserRepository
from webapp.domain.auth.persistance.token_repository import TokenRepository
from webapp.domain.auth.third_party import kakao_login_client


class AuthService:
    def __init__(
            self,
            user_repository: UserRepository,
            kakao_repository: KakaoRepository,
            token_repository: TokenRepository
    ):
        self.user_repository = user_repository
        self.kakao_repository = kakao_repository
        self.token_repository = token_repository

    def _register(self, kakao_id: int, nickname: str, profile_image_url: str):
        user = User.create(
            nickname=nickname,
            profile_image_url=profile_image_url
        )

        kakao = Kakao.create(
            kakao_id=kakao_id,
            user_id=user.id
        )

        self.user_repository.save(user)
        self.kakao_repository.save(kakao)

        return user.id

    def login(self, access_token) -> (str, str):
        kakao_user_info = kakao_login_client.get_user_info(access_token)
        try:
            kakao = self.kakao_repository.find_by_id(kakao_id=kakao_user_info.id)
            user_id = kakao.user_id
        except persistence.ResourceNotFound:
            user_id = self._register(
                kakao_id=kakao_user_info.id,
                nickname=kakao_user_info.nickname,
                profile_image_url=kakao_user_info.profile_image_url
            )

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

        token.access_token = create_access_token(token.user_id)
        if exp - datetime.now() < timedelta(days=30):
            token.refresh_token = create_refresh_token(token_id)

        self.token_repository.save(token)

        return (
            token.access_token,
            token.refresh_token
        )
