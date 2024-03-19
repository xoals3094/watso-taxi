from dependency_injector import containers, providers
from pymongo import MongoClient
from config.production import mongodb

from domain.taxi.group.application.group_service import GroupService
from domain.taxi.group.persistance.repository import MongoDBGroupRepository
from domain.taxi.group.persistance.group_query_dao import MongoDBGroupQueryDao
from domain.taxi.group.persistance.group_update_dao import MongoDBGroupUpdateDao

from domain.taxi.point.persistance.point_query_dao import MongoDBPointQueryDao


class TaxiContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=['app.api.taxi.group',
                                                            'app.api.taxi.point'])

    mongodb_connection = providers.Singleton(
        MongoClient,
        host=mongodb.host,
        username=mongodb.username,
        password=mongodb.password,
        port=mongodb.port,
        connect=False
    )

    group_repository = providers.Singleton(MongoDBGroupRepository, mongodb_connection)
    group_query_dao = providers.Singleton(MongoDBGroupQueryDao, mongodb_connection)
    group_update_dao = providers.Singleton(MongoDBGroupUpdateDao, mongodb_connection)
    point_query_dao = providers.Singleton(MongoDBPointQueryDao, mongodb_connection)

    group_service = providers.Singleton(GroupService, group_repository=group_repository, group_update_dao=group_update_dao)
