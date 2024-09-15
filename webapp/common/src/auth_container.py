from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Factory, Resource
from webapp.common import database
from webapp.domain.auth.persistance.token_repository import TokenRepository
from webapp.domain.auth.persistance.kakao_repository import KakaoRepository
from webapp.domain.auth.application.auth_service import AuthService


class AuthContainer(DeclarativeContainer):
    wiring_config = WiringConfiguration(modules=['webapp.endpoint.auth'])

    session = Resource(database.get_session)

    kakao_repository = Factory(KakaoRepository, session=session)
    token_repository = Factory(TokenRepository, session=session)

    auth_service = Factory(
        AuthService,
        kakao_repository=kakao_repository,
        token_repository=token_repository
    )
