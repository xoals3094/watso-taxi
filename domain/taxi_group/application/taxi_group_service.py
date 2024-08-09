from datetime import datetime
from domain.group.application.group_service import GroupService
from domain.group.persistance.group_repository import MySQLGroupRepository
from domain.taxi_group.persistance.bill_dao import MySQLBillDao
from domain.taxi_group.entity.taxi_group import TaxiGroup
from domain.taxi_group.persistance.taxi_group_repository import MySQLTaxiGroupRepository
from domain.taxi_group.entity.status import Status
from domain.taxi_group.entity.bill import Bills


class TaxiGroupService:
    def __init__(self,
                 group_service: GroupService,
                 group_repository: MySQLGroupRepository,
                 taxi_group_repository: MySQLTaxiGroupRepository,
                 bill_dao: MySQLBillDao):
        self.group_service = group_service
        self.group_repository = group_repository
        self.taxi_group_repository = taxi_group_repository
        self.bill_dao = bill_dao

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
        self.bill_dao.insert_bill(group_id=group_id, user_id=owner_id)
        return group_id

    def update_bill(self, group_id: int, fee: int, bills: Bills):
        group = self.group_repository.find_group_by_id(group_id)
        taxi_group = self.taxi_group_repository.find_taxi_group_by_id(group_id)

        bills.verify(fee=fee, members=group.member.members)

        taxi_group.set_fee(fee)
        self.taxi_group_repository.update_fee(group_id, taxi_group.fee)
        self.bill_dao.update_bills(group_id, bills)

    def open(self, group_id):
        taxi_group = self.taxi_group_repository.find_taxi_group_by_id(group_id)
        taxi_group.set_status(Status.OPEN)
        self.group_service.open(group_id)
        self.taxi_group_repository.update_status(group_id, taxi_group.status)

    def close(self, group_id):
        taxi_group = self.taxi_group_repository.find_taxi_group_by_id(group_id)
        taxi_group.set_status(Status.CLOSE)
        self.group_service.close(group_id)
        self.taxi_group_repository.update_status(group_id, taxi_group.status)

    def settle(self, group_id: int):
        group = self.group_repository.find_group_by_id(group_id)
        taxi_group = self.taxi_group_repository.find_taxi_group_by_id(group_id)
        bills = self.bill_dao.find_bills_by_group_id(group_id)

        bills.verify(fee=taxi_group.fee, members=group.member.members)
        taxi_group.set_status(Status.SETTLE)

        self.taxi_group_repository.update_status(group_id, taxi_group.status)

    def complete(self, group_id: int):
        taxi_group = self.taxi_group_repository.find_taxi_group_by_id(group_id)
        taxi_group.set_status(Status.COMPLETE)

        # 완료 코드

        self.taxi_group_repository.update_status(group_id, taxi_group.status)

    def participate(self, group_id, user_id):
        self.group_service.participate(group_id, user_id)
        self.bill_dao.insert_bill(group_id, user_id)

        group = self.group_repository.find_group_by_id(group_id)
        taxi_group = self.taxi_group_repository.find_taxi_group_by_id(group_id)

        bills = self.bill_dao.find_bills_by_group_id(group_id)
        bills.divide(owner_id=group.owner_id, fee=taxi_group.fee)

        self.bill_dao.update_bills(group_id, bills)

    def leave(self, group_id, user_id):
        self.group_service.leave(group_id, user_id)
        self.bill_dao.delete_bill(group_id, user_id)

        group = self.group_repository.find_group_by_id(group_id)
        taxi_group = self.taxi_group_repository.find_taxi_group_by_id(group_id)

        bills = self.bill_dao.find_bills_by_group_id(group_id)
        bills.divide(owner_id=group.owner_id, fee=taxi_group.fee)

        self.bill_dao.update_bills(group_id, bills)
