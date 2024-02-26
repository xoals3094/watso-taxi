from dependency_injector import containers, providers
from pymongo import MongoClient
from config.production import mongodb

from logic.taxi.post.application.PostWriteService import PostWriteService
from logic.taxi.post.application.PostQueryService import PostQueryService
from logic.taxi.point.application.PointQueryService import PointQueryService

from logic.taxi.post.adapter.outgoing.PostRepository import MongoDBPostRepository
from logic.taxi.post.adapter.outgoing.PostQueryAdapter import MongoDBPostQueryDao
from logic.taxi.post.adapter.outgoing.PostUpdateAdapter import MongoDBPostUpdateDao
from logic.taxi.point.adapter.outgoing.PointQueryAdapter import MongoDBPointQueryDao


class TaxiContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=['app.api.taxi.post',
                                                            'app.api.taxi.point'])

    mongodb_connection = providers.Singleton(
        MongoClient,
        host=mongodb.host,
        username=mongodb.username,
        password=mongodb.password,
        port=mongodb.port,
        connect=False
    )

    post_repository = providers.Singleton(MongoDBPostRepository, mongodb_connection)
    post_query_dao = providers.Singleton(MongoDBPostQueryDao, mongodb_connection)
    post_update_dao = providers.Singleton(MongoDBPostUpdateDao, mongodb_connection)
    point_query_dao = providers.Singleton(MongoDBPointQueryDao, mongodb_connection)

    post_query_service = providers.Singleton(PostQueryService, post_query_dao=post_query_dao)
    post_write_service = providers.Singleton(PostWriteService, post_repository=post_repository, post_update_dao=post_update_dao)
    point_query_service = providers.Singleton(PointQueryService, point_query_dao=point_query_dao)
