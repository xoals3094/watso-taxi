from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Factory, Resource
from webapp.common import database

from webapp.domain.auth.persistance.token_repository import TokenRepository
from webapp.domain.auth.persistance.kakao_repository import KakaoRepository
from webapp.domain.auth.application.jwt_auth_service import JWTAuthService
from webapp.domain.auth.application.kakao_auth_service import KakaoAuthService

from webapp.domain.user.persistance.user_repository import UserRepository
from webapp.domain.user.application.user_service import UserService

from webapp.domain.taxi_group.application.taxi_group_service import TaxiGroupService
from webapp.domain.taxi_group.persistance.taxi_group_repository import TaxiGroupRepository
from webapp.domain.taxi_group.application.query_service import QueryService
from webapp.domain.taxi_group.persistance.taxi_group_dao import TaxiGroupDao


class Container(DeclarativeContainer):
    wiring_config = WiringConfiguration(
        modules=[
            'webapp.endpoint.auth',
            'webapp.endpoint.taxi',
            'webapp.endpoint.user'
        ]
    )

    session = Resource(database.get_session)

    kakao_repository = Factory(KakaoRepository, session=session)
    token_repository = Factory(TokenRepository, session=session)
    user_repository = Factory(UserRepository, session=session)
    taxi_group_repository = Factory(TaxiGroupRepository, session=session)
    taxi_group_dao = Factory(TaxiGroupDao, session=session)

    user_service = Factory(UserService, user_repository=user_repository)
    jwt_auth_service = Factory(JWTAuthService, token_repository=token_repository)
    kakao_auth_service = Factory(
        KakaoAuthService,
        user_service=user_service,
        jwt_auth_service=jwt_auth_service,
        kakao_repository=kakao_repository,
    )

    taxi_group_service = Factory(
        TaxiGroupService,
        taxi_group_repository=taxi_group_repository
    )
    query_service = Factory(QueryService, taxi_group_dao=taxi_group_dao)
