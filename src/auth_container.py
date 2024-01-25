from dependency_injector import containers, providers
from pymongo import MongoClient
from config.production import mongodb


from logic.auth.adapter.outgoing.UserAdapter import MongoDBUserDao
from logic.auth.application.KakaoLoginService import KakaoLoginService
from logic.auth.adapter.outgoing.KakaoApiAdapter import ApiKakaoAdapter


class AuthContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=['app.auth.auth'])

    mongodb_connection = providers.Singleton(
        MongoClient,
        host=mongodb.host,
        #username=mongodb.username,
        #password=mongodb.password,
        port=mongodb.port,
        connect=False
    )

    kakao_dao = providers.Singleton(ApiKakaoAdapter)
    user_dao = providers.Singleton(MongoDBUserDao, mongodb_connection=mongodb_connection)

    kakao_service = providers.Singleton(KakaoLoginService, kakao_dao=kakao_dao, user_dao=user_dao)
