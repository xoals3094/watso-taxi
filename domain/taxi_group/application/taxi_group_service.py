from datetime import datetime

from domain.group.application.group_service import GroupService
from domain.taxi_group.entity.taxi_group import TaxiGroup
from domain.group.application.group_repository import GroupRepository
from domain.taxi_group.persistance.taxi_group_repository import MySQLTaxiGroupRepository
from domain.taxi_group.entity.status import Status
from domain.taxi_group.entity.bill import Bill


class TaxiGroupService:
    def __init__(self, group_service: GroupService, group_repository: GroupRepository, taxi_group_repository: MySQLTaxiGroupRepository):
        self.group_service = group_service
        self.group_repository = group_repository
        self.taxi_group_repository = taxi_group_repository

    def create(self,
               owner_id: int,
               max_member: int,
               depart_datetime: datetime,
               direction: str) -> int:
        group_id = self.group_service.create(owner_id, max_member)
        taxi_group = TaxiGroup.create(group_id=group_id,
                                      depart_datetime=depart_datetime,
                                      direction=direction)
        self.taxi_group_repository.save(taxi_group)

        return group_id

    def recruit(self, group_id):
        taxi_group = self.taxi_group_repository.find_taxi_group_by_id(group_id)
        taxi_group.set_status(Status.RECRUITING)
        self.group_service.open(group_id)
        self.taxi_group_repository.update_status(group_id, taxi_group.status)

    def close(self, group_id):
        taxi_group = self.taxi_group_repository.find_taxi_group_by_id(group_id)
        taxi_group.set_status(Status.CLOSED)
        self.group_service.close(group_id)
        self.taxi_group_repository.update_status(group_id, taxi_group.status)

    def settle(self, group_id: int, bill: Bill):
        group = self.group_repository.find_group_by_id(group_id)
        taxi_group = self.taxi_group_repository.find_taxi_group_by_id(group_id)
        taxi_group.set_status(Status.SETTLEMENT)

        users = bill.get_members()
        group.verify_users(users)

        total_cost = bill.get_total_cost()
        taxi_group.verify_fee(total_cost)

        # 정산 코드

    def complete(self, group_id: int):
        taxi_group = self.taxi_group_repository.find_taxi_group_by_id(group_id)
        taxi_group.set_status(Status.COMPLETED)

        # 완료 코드
