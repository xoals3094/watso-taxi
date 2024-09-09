from datetime import datetime
from webapp.endpoint.models.taxi import FeeUpdate
from webapp.domain.group.service import GroupService
from webapp.domain.taxi.application.bill_service import BillService
from webapp.domain.taxi.entity.taxi_group import TaxiGroup
from webapp.domain.taxi.entity.status import Status
from webapp.domain.taxi.entity.bill import Bill

from webapp.domain.taxi.persistance.taxi_group_repository import MySQLTaxiGroupRepository


class TaxiGroupService:

    def __init__(
            self,
            group_service: GroupService,
            taxi_group_repository: MySQLTaxiGroupRepository,
            bill_service: BillService
    ):
        self.group_service = group_service
        self.taxi_group_repository = taxi_group_repository
        self.bill_service = bill_service

    def create(
            self,
            owner_id: int,
            max_member: int,
            depart_datetime: datetime,
            direction: str
    ) -> int:
        group_id = self.group_service.create(owner_id, max_member)
        taxi_group = TaxiGroup.create(
            group_id=group_id,
            depart_datetime=depart_datetime,
            direction=direction
        )
        self.taxi_group_repository.save(taxi_group)
        self.bill_service.create_bill(group_id=group_id, user_id=owner_id)
        return group_id

    def set_fee(
            self,
            group_id: int,
            fee: int,
            bills: list[FeeUpdate.Bill]
    ):
        taxi_group = self.taxi_group_repository.find_taxi_group_by_id(group_id)
        taxi_group.set_fee(fee)

        bills = [
            Bill(user_id=bill.user_id, cost=bill.cost)
            for bill in bills
        ]
        
        self.bill_service.set_bill(group_id, bills)
        self.taxi_group_repository.update_fee(group_id, taxi_group.fee)

    def open(
            self,
            group_id
    ):
        taxi_group = self.taxi_group_repository.find_taxi_group_by_id(group_id)
        taxi_group.set_status(Status.OPEN)
        self.group_service.open(group_id)
        self.taxi_group_repository.update_status(group_id, taxi_group.status)

    def close(
            self,
            group_id
    ):
        taxi_group = self.taxi_group_repository.find_taxi_group_by_id(group_id)
        taxi_group.set_status(Status.CLOSE)
        self.group_service.close(group_id)
        self.taxi_group_repository.update_status(group_id, taxi_group.status)

    def settle(
            self,
            group_id: int
    ):
        taxi_group = self.taxi_group_repository.find_taxi_group_by_id(group_id)
        taxi_group.set_status(Status.SETTLE)
        self.taxi_group_repository.update_status(group_id, taxi_group.status)

    def complete(
            self,
            group_id: int
    ):
        taxi_group = self.taxi_group_repository.find_taxi_group_by_id(group_id)
        taxi_group.set_status(Status.COMPLETE)
        self.taxi_group_repository.update_status(group_id, taxi_group.status)

    def participate(
            self,
            group_id,
            user_id
    ):
        self.group_service.participate(group_id, user_id)
        self.bill_service.create_bill(group_id, user_id)

    def leave(
            self,
            group_id,
            user_id
    ):
        self.group_service.leave(group_id, user_id)
        self.bill_service.remove_bill(group_id, user_id)
