from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Factory, Resource
from webapp.common import database
from webapp.domain.user.persistance.user_repository import UserRepository
from webapp.domain.user.application.user_service import UserService
from webapp.domain.auth.persistance.token_repository import TokenRepository
from webapp.domain.auth.persistance.kakao_repository import KakaoRepository
from webapp.domain.auth.application.jwt_auth_service import JWTAuthService
from webapp.domain.auth.application.kakao_auth_service import KakaoAuthService


class AuthContainer(DeclarativeContainer):
    wiring_config = WiringConfiguration(modules=['webapp.endpoint.auth'])

    session = Resource(database.get_session)

    user_repository = Factory(UserRepository, session=session)
    kakao_repository = Factory(KakaoRepository, session=session)
    token_repository = Factory(TokenRepository, session=session)

    user_service = Factory(UserService, user_repository=user_repository)
    jwt_auth_service = Factory(JWTAuthService, token_repository=token_repository)
    kakao_auth_service = Factory(
        KakaoAuthService,
        user_service=user_service,
        jwt_auth_service=jwt_auth_service,
        kakao_repository=kakao_repository,
    )
