from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Factory, Resource
from webapp.common import database

from webapp.domain.auth.persistance.user_repository import UserRepository
from webapp.domain.auth.persistance.token_repository import TokenRepository
from webapp.domain.auth.persistance.kakao_repository import KakaoRepository
from webapp.domain.auth.application.auth_service import AuthService


class AuthContainer(DeclarativeContainer):
    wiring_config = WiringConfiguration(modules=['webapp.endpoint.auth'])

    mysql_connection = Resource(database.get_connection)

    user_repository = Factory(UserRepository, mysql_connection=mysql_connection)
    kakao_repository = Factory(KakaoRepository, mysql_connection=mysql_connection)
    token_repository = Factory(TokenRepository, mysql_connection=mysql_connection)

    auth_service = Factory(AuthService, user_repository=user_repository, token_repository=token_repository)
