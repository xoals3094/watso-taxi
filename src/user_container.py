from dependency_injector import containers, providers
from pymongo import MongoClient
from redis import StrictRedis
from config.production import mongodb, redis


from logic.user.adapter.outgoing.UserRepository import MongoDBUserRepository
from logic.user.adapter.outgoing.UserAdapter import MongoDBUserDao
from logic.user.adapter.outgoing.TokenAdapter import MongoDBTokenDao
from logic.user.adapter.outgoing.CodeCacheAdapter import RedisCodeCacher
from logic.user.adapter.outgoing.DeviceAdapter import MongoDBDeviceDao

from logic.user.application.SignupService import SignupService, SignupAuthService
from logic.user.application.UserService import UserService
from logic.user.application.ForgotService import ForgotPasswordService, ForgotUsernameService
from logic.user.application.AuthService import JwtAuthService
from logic.user.application.ProfileService import ProfileQueryService, ProfileUpdateService, ProfileDeleteService
from logic.user.application.DeviceService import DeviceService


class UserContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=['app.user.forgot',
                                                            'app.user.profile',
                                                            'app.user.signup',
                                                            'app.user.user',
                                                            'app.user.device',
                                                            'app.auth.login',
                                                            'app.auth.logout',
                                                            'app.auth.refresh'])

    redis_connection = providers.Singleton(
        StrictRedis,
        host=redis.host,
        port=redis.port,
        password=redis.pwd,
        db=redis.post_db,
        decode_responses=True
    )

    mongodb_connection = providers.Singleton(
        MongoClient,
        host=mongodb.host,
        username=mongodb.user,
        password=mongodb.pwd,
        port=mongodb.port,
        connect=False
    )

    user_repository = providers.Singleton(MongoDBUserRepository, mongodb_connection=mongodb_connection)
    user_dao = providers.Singleton(MongoDBUserDao, mongodb_connection=mongodb_connection)
    token_dao = providers.Singleton(MongoDBTokenDao, mongodb_connection=mongodb_connection)
    code_cacher = providers.Singleton(RedisCodeCacher, redis_connection=redis_connection)
    device_dao = providers.Singleton(MongoDBDeviceDao, mongodb_connection=mongodb_connection)

    signup_service = providers.Singleton(SignupService, user_repository=user_repository, code_cacher=code_cacher)
    signup_auth_service = providers.Singleton(SignupAuthService, code_cacher=code_cacher)

    user_service = providers.Singleton(UserService, user_dao=user_dao)

    forgot_username_service = providers.Singleton(ForgotUsernameService, user_repository=user_repository)
    forgot_password_service = providers.Singleton(ForgotPasswordService, user_dao=user_dao, user_repository=user_repository)

    auth_service = providers.Singleton(JwtAuthService, user_repository=user_repository, token_dao=token_dao)

    profile_query_service = providers.Singleton(ProfileQueryService, user_repository=user_repository)
    profile_delete_service = providers.Singleton(ProfileDeleteService, user_repository=user_repository)
    profile_update_service = providers.Singleton(ProfileUpdateService, user_repository=user_repository, user_dao=user_dao)

    device_service = providers.Singleton(DeviceService, device_dao=device_dao)
