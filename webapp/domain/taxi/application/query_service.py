from datetime import datetime
from webapp.domain.taxi.persistance.taxi_group_query_dao import MySQLTaxiGroupQueryDao
from webapp.endpoint.models.taxi import (
    GroupQueryOption,
    Direction
)


class QueryService:
    def __init__(self, taxi_group_query_dao: MySQLTaxiGroupQueryDao):
        self.taxi_group_query_dao = taxi_group_query_dao

    def get_taxi_group(self):
        pass

    def get_taxi_group_list(
            self,
            option: GroupQueryOption,
            direction: Direction,
            user_id: int,
            departure_datetime: datetime
    ):
        if option == GroupQueryOption.JOINABLE:
            self.taxi_group_query_dao.find_joinable_groups(
                user_id=user_id,
                direction=direction,
                departure_datetime=departure_datetime
            )

        elif option == GroupQueryOption.JOINED:
            self.taxi_group_query_dao.find_joined_groups(user_id=user_id)
