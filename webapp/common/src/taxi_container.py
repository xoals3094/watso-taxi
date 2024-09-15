from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Factory, Resource
from webapp.common import database

from webapp.domain.taxi_group.application.taxi_group_service import TaxiGroupService
from webapp.domain.taxi_group.persistance.taxi_group_repository import TaxiGroupRepository
from webapp.domain.taxi_group.application.query_service import QueryService
from webapp.domain.taxi_group.persistance.taxi_group_dao import TaxiGroupDao


class TaxiContainer(DeclarativeContainer):
    wiring_config = WiringConfiguration(
        modules=[
            'webapp.endpoint.taxi'
        ]
    )

    session = Resource(database.get_session)

    taxi_group_repository = Factory(TaxiGroupRepository, session=session)
    taxi_group_service = Factory(
        TaxiGroupService,
        taxi_group_repository=taxi_group_repository
    )

    taxi_group_dao = Factory(TaxiGroupDao, session=session)
    query_service = Factory(QueryService, taxi_group_dao=taxi_group_dao)
