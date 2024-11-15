from datetime import datetime
from webapp.domain.taxi_group.persistance.taxi_group_dao import TaxiGroupDao
from webapp.endpoint.models.taxi import (
    TaxiGroupDetail,
    TaxiGroupSummary,
    GroupQueryOption,
    Direction,
    FareDetail
)

DEFAULT_FARE = 8300


class QueryService:
    def __init__(self, taxi_group_dao: TaxiGroupDao):
        self.taxi_group_dao = taxi_group_dao

    def get_taxi_group(
            self,
            group_id: str,
            user_id: str
    ) -> TaxiGroupDetail:

        id, role, current_member, max_members, status, departure_datetime, direction, fee, cost = self.taxi_group_dao.find_taxi_group_detail_by_id(user_id, group_id)
        return TaxiGroupDetail.mapping(
            id=id,
            role=role,
            status=status,
            direction=direction,
            departure_datetime=departure_datetime,
            current_members=current_member,
            max_members=max_members,
            fare=fee if fee is not None else DEFAULT_FARE,
            cost=cost if cost is not None else DEFAULT_FARE // current_member
        )

    def get_taxi_group_list(
            self,
            option: GroupQueryOption,
            direction: Direction,
            user_id: str,
            departure_datetime: datetime
    ) -> list[TaxiGroupSummary]:

        results = []
        if option == GroupQueryOption.JOINED:
            taxi_groups = self.taxi_group_dao.find_joined(user_id, departure_datetime)
            for id, current_member, max_members, status, departure_datetime, direction, fee, cost in taxi_groups:
                taxi_group = TaxiGroupSummary.mapping(
                    id=id,
                    current_members=current_member,
                    max_members=max_members,
                    status=status,
                    departure_datetime=departure_datetime,
                    direction=direction,
                    fare=fee if fee is not None else DEFAULT_FARE,
                    cost=cost if cost is not None else DEFAULT_FARE // current_member
                )
                results.append(taxi_group)

        elif option == GroupQueryOption.JOINABLE:
            taxi_groups = self.taxi_group_dao.find_joinable(user_id, direction, departure_datetime)
            for id, current_member, max_members, status, departure_datetime, direction in taxi_groups:
                taxi_group = TaxiGroupSummary.mapping(
                    id=id,
                    current_members=current_member,
                    max_members=max_members,
                    status=status,
                    departure_datetime=departure_datetime,
                    direction=direction,
                    fare=DEFAULT_FARE,
                    cost=DEFAULT_FARE // (current_member + 1)
                )
                results.append(taxi_group)

        return results

    def get_history(self, user_id) -> list[TaxiGroupSummary]:
        taxi_groups = self.taxi_group_dao.find_complete(user_id)

        results = []
        for id, current_member, max_members, status, departure_datetime, direction, fee, cost in taxi_groups:
            taxi_group = TaxiGroupSummary.mapping(
                id=id,
                current_members=current_member,
                max_members=max_members,
                status=status,
                departure_datetime=departure_datetime,
                direction=direction,
                fare=fee,
                cost=cost
            )
            results.append(taxi_group)

        return results

    def get_fare(
            self,
            group_id: str
    ) -> FareDetail:
        fare, members = self.taxi_group_dao.find_fare(group_id)
        return FareDetail.mapping(fare=fare, members=members)
