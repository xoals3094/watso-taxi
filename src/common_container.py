from dependency_injector import containers, providers
from pymongo import MongoClient
from redis import StrictRedis
from config.production import mongodb, redis


from logic.common.push_message.adapter.outgoing.TokenQueryAdapter import MongoDBTokenQueryDao
from logic.common.push_message.adapter.outgoing.UserIdFindAdapter import MongoDBUserIdFinder
from logic.common.push_message.adapter.outgoing.MessagePusherAdapter import FirebaseMessagePusher
from logic.common.email.adapter.outgoing.GoogleEmailSendAdapter import GoogleEmailSender


class CommonContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=['logic.common.push_message.application.PostEventHandler',
                                                            'logic.common.push_message.application.CommentEventHandler',
                                                            'logic.common.email.application.SignupSignalHandler',
                                                            'logic.common.email.application.ForgotSignalHandler'])

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

    user_id_finder = providers.Singleton(MongoDBUserIdFinder, mongodb_connection=mongodb_connection)
    token_query_dao = providers.Singleton(MongoDBTokenQueryDao, mongodb_connection=mongodb_connection)
    message_pusher = providers.Singleton(FirebaseMessagePusher)
    email_sender = providers.Singleton(GoogleEmailSender)
