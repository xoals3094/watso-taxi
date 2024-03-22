from dependency_injector import containers, providers
from pymongo import MongoClient
from config.production import mongodb


from domain.auth.persistance.user_dao import MongoDBUserDao
from domain.auth.persistance.kakao_dao import ApiKakaoDao
from domain.auth.application.kakao_login_service import KakaoLoginService


class AuthContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=['app.api.auth.auth'])

    mongodb_connection = providers.Singleton(
        MongoClient,
        host=mongodb.host,
        username=mongodb.username,
        password=mongodb.password,
        port=mongodb.port,
        connect=False
    )

    kakao_dao = providers.Singleton(ApiKakaoDao)
    user_dao = providers.Singleton(MongoDBUserDao, mongodb_connection=mongodb_connection)

    kakao_service = providers.Singleton(KakaoLoginService, kakao_dao=kakao_dao, user_dao=user_dao)
