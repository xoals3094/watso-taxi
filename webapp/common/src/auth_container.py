from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Factory, Resource
from webapp.common import database

from webapp.domain.auth.persistance.user_dao import MySQLUserDao
from webapp.domain.auth.persistance.token_dao import MySQLTokenDao
from webapp.domain.auth.application.jwt_login_service import JWTLoginService
from webapp.domain.auth.application.kakao_login_service import KakaoLoginService


class AuthContainer(DeclarativeContainer):
    wiring_config = WiringConfiguration(modules=['webapp.endpoint.auth'])

    mysql_connection = Resource(database.get_connection)

    user_dao = Factory(MySQLUserDao, mysql_connection=mysql_connection)
    token_dao = Factory(MySQLTokenDao, mysql_connection=mysql_connection)

    kakao_service = Factory(KakaoLoginService, user_dao=user_dao, token_dao=token_dao)
    jwt_login_service = Factory(JWTLoginService, token_dao=token_dao)
