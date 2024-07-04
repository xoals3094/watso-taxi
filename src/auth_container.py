from dependency_injector import containers, providers
from pymysql import connect
from config.production import mysql
from domain.auth.persistance.user_dao import MySQLUserDao
from domain.auth.persistance.kakao_dao import ApiKakaoDao
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

    kakao_dao = providers.Singleton(ApiKakaoDao)
    user_dao = providers.Singleton(MySQLUserDao, mysql_connection=mysql_connection)

    kakao_service = providers.Singleton(KakaoLoginService, kakao_dao=kakao_dao, user_dao=user_dao)
