from dependency_injector import containers, providers
from pymongo import MongoClient
from config.production import mongodb


from logic.auth.adapter.outgoing.UserRepository import MongoDBUserRepository
from logic.auth.adapter.outgoing.TokenAdapter import MongoDBTokenDao
from logic.auth.application.AuthService import JwtAuthService


class AuthContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=['app.auth.auth'])

    mongodb_connection = providers.Singleton(
        MongoClient,
        host=mongodb.host,
        username=mongodb.username,
        password=mongodb.password,
        port=mongodb.port,
        connect=False
    )

    user_repository = providers.Singleton(MongoDBUserRepository, mongodb_connection=mongodb_connection)
    token_dao = providers.Singleton(MongoDBTokenDao, mongodb_connection=mongodb_connection)

    auth_service = providers.Singleton(JwtAuthService, user_repository=user_repository, token_dao=token_dao)

