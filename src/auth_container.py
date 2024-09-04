from dependency_injector import containers, providers
from pymysql import connect
from config import mysql
from domain.auth.persistance.user_dao import MySQLUserDao
from domain.auth.persistance.token_dao import MySQLTokenDao
from domain.auth.application.jwt_login_service import JWTLoginService
from domain.auth.application.kakao_login_service import KakaoLoginService


class AuthContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=['app.api.auth.auth'])
    mysql_connection = providers.Singleton(
        connect,
        host=mysql.host,
        user=mysql.user,
        password=mysql.password,
        port=mysql.port,
        database=mysql.database
    )

    user_dao = providers.Singleton(MySQLUserDao, mysql_connection=mysql_connection)
    token_dao = providers.Singleton(MySQLTokenDao, mysql_connection=mysql_connection)

    kakao_service = providers.Singleton(KakaoLoginService, user_dao=user_dao, token_dao=token_dao)
    jwt_login_service = providers.Singleton(JWTLoginService, token_dao=token_dao)
