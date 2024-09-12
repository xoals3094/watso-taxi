from datetime import datetime
from typing import List
from webapp.domain.group.service import GroupService
from webapp.domain.taxi_group.entity.taxi_group import TaxiGroup, TaxiMember
from webapp.domain.taxi_group.persistance.taxi_group_repository import TaxiGroupRepository
from webapp.endpoint.models.taxi import FareUpdate


class TaxiGroupService(GroupService):
    def __init__(self, taxi_group_repository: TaxiGroupRepository):
        self.taxi_group_repository = taxi_group_repository

    def create(
            self,
            *,
            owner_id: int,
            departure_datetime: datetime,
            direction: str,
            max_members: int
    ) -> int:
        taxi_group = TaxiGroup.create(
            owner_id=owner_id,
            departure_datetime=departure_datetime,
            direction=direction,
            max_members=max_members
        )
        self.taxi_group_repository.save(taxi_group)
        return taxi_group.id

    def open(self, group_id):
        taxi_group = self.taxi_group_repository.find_by_id(group_id)
        taxi_group.open()
        self.taxi_group_repository.save(taxi_group)

    def close(self, group_id):
        taxi_group = self.taxi_group_repository.find_by_id(group_id)
        taxi_group.close()
        self.taxi_group_repository.save(taxi_group)

    def settle(self, group_id: int):
        taxi_group = self.taxi_group_repository.find_by_id(group_id)
        taxi_group.settle()
        self.taxi_group_repository.save(taxi_group)

    def complete(self, group_id: int):
        taxi_group = self.taxi_group_repository.find_by_id(group_id)
        taxi_group.complete()
        self.taxi_group_repository.save(taxi_group)

    def participate(self, group_id, user_id):
        taxi_group = self.taxi_group_repository.find_by_id(group_id)
        taxi_group.participate(user_id)
        self.taxi_group_repository.save(taxi_group)

    def leave(self, group_id, user_id):
        taxi_group = self.taxi_group_repository.find_by_id(group_id)
        taxi_group.leave(user_id)
        self.taxi_group_repository.save(taxi_group)

    def update_fare(
            self,
            group_id: int,
            fare: int,
            members: List[FareUpdate.Member]
    ):
        taxi_group = self.taxi_group_repository.find_by_id(group_id)

        members = [TaxiMember(member.id, member.cost) for member in members]
        taxi_group.set_fare(fare, members)
        self.taxi_group_repository.save(taxi_group)

