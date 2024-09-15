from datetime import datetime
from webapp.domain.taxi_group.persistance.taxi_group_dao import TaxiGroupDao
from webapp.endpoint.models.taxi import (
    TaxiGroup,
    GroupQueryOption,
    Direction,
    FareDetail
)


class QueryService:
    def __init__(self, taxi_group_dao: TaxiGroupDao):
        self.taxi_group_dao = taxi_group_dao

    def get_taxi_group(
            self,
            group_id: str,
            user_id: str
    ) -> TaxiGroup:
        taxi_group = self.taxi_group_dao.find_by_id(group_id)
        return TaxiGroup.mapping(user_id, taxi_group)

    def get_taxi_group_list(
            self,
            option: GroupQueryOption,
            direction: Direction,
            user_id: str,
            departure_datetime: datetime
    ) -> list[TaxiGroup]:

        results = []
        if option == GroupQueryOption.JOINED:
            taxi_groups = self.taxi_group_dao.find_joined(user_id, departure_datetime)
            for taxi_group in taxi_groups:
                taxi_group = TaxiGroup.mapping(user_id=user_id, taxi_group=taxi_group)
                results.append(taxi_group)

        elif option == GroupQueryOption.JOINABLE:
            taxi_groups = self.taxi_group_dao.find_joinable(user_id, direction, departure_datetime)
            for taxi_group in taxi_groups:
                taxi_group = TaxiGroup.mapping(user_id=user_id, taxi_group=taxi_group)
                results.append(taxi_group)

        return results

    def get_history(self, user_id) -> list[TaxiGroup]:
        taxi_groups = self.taxi_group_dao.find_complete(user_id)

        results = []
        for taxi_group in taxi_groups:
            taxi_group = TaxiGroup.mapping(user_id=user_id, taxi_group=taxi_group)
            results.append(taxi_group)

        return results

    def get_fare(
            self,
            group_id: str
    ) -> FareDetail:
        fare, members = self.taxi_group_dao.find_fare(group_id)
        return FareDetail.mapping(fare=fare, members=members)
