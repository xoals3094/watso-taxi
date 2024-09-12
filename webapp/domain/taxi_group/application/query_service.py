from datetime import datetime
from webapp.domain.taxi_group.persistance.taxi_group_dao import MySQLTaxiGroupDao
from webapp.endpoint.models.taxi import (
    TaxiGroup,
    GroupQueryOption,
    Direction,
    FareDetail
)


class QueryService:
    def __init__(self, taxi_group_dao: MySQLTaxiGroupDao):
        self.taxi_group_dao = taxi_group_dao

    def get_taxi_group(
            self,
            group_id: int,
            user_id: int
    ) -> TaxiGroup:

        pass

    def get_taxi_group_list(
            self,
            option: GroupQueryOption,
            direction: Direction,
            user_id: int,
            departure_datetime: datetime
    ) -> list[TaxiGroup]:

        pass

    def get_fare(
            self,
            group_id: int
    ) -> FareDetail:

        pass
