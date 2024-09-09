from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Factory, Resource
from webapp.common import database

from webapp.domain.group.service import GroupService
from webapp.domain.group.repository import MySQLGroupRepository

from webapp.domain.taxi.application.query_service import QueryService
from webapp.domain.taxi.persistance.taxi_group_query_dao import MySQLTaxiGroupQueryDao

from webapp.domain.taxi.application.taxi_group_service import TaxiGroupService
from webapp.domain.taxi.persistance.taxi_group_repository import MySQLTaxiGroupRepository

from webapp.domain.taxi.application.bill_service import BillService
from webapp.domain.taxi.persistance.bill_dao import MySQLBillDao
from webapp.domain.taxi.persistance.group_dao import MySQLGroupDao


class TaxiContainer(DeclarativeContainer):
    wiring_config = WiringConfiguration(modules=['webapp.endpoint.taxi'])

    mysql_connection = Resource(database.get_connection)

    group_repository = Factory(MySQLGroupRepository, mysql_connection=mysql_connection)
    taxi_group_repository = Factory(MySQLTaxiGroupRepository, mysql_connection=mysql_connection)
    taxi_group_query_dao = Factory(MySQLTaxiGroupQueryDao, mysql_connection=mysql_connection)
    bill_dao = Factory(MySQLBillDao, mysql_connection=mysql_connection)
    group_dao = Factory(MySQLGroupDao, mysql_connection=mysql_connection)

    group_service = Factory(GroupService, group_repository=group_repository)
    bill_service = Factory(BillService, group_dao=group_dao, bill_dao=bill_dao)
    taxi_group_service = Factory(
        TaxiGroupService,
        group_service=group_service,
        taxi_group_repository=taxi_group_repository,
        bill_service=bill_service
    )

    query_service = Factory(QueryService, taxi_group_query_dao=taxi_group_query_dao)
