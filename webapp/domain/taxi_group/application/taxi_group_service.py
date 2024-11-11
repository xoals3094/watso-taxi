from datetime import datetime
from webapp.domain.taxi_group.entity.taxi_group import TaxiGroup
from webapp.domain.taxi_group.entity.billing_policy import AutoBillingPolicy, CustomBillingPolicy
from webapp.domain.chat.chat_group_processor import ChatGroupProcessor
from webapp.domain.taxi_group.persistance.taxi_group_repository import TaxiGroupRepository
from webapp.domain.taxi_group.persistance.bill_repository import BillRepository


class TaxiGroupService:
    def __init__(
            self,
            chat_group_processor: ChatGroupProcessor,
            taxi_group_repository: TaxiGroupRepository,
            bill_repository: BillRepository
    ):
        self.chat_group_processor = chat_group_processor
        self.taxi_group_repository = taxi_group_repository
        self.bill_repository = bill_repository

    def create(
            self,
            *,
            owner_id: str,
            departure_datetime: datetime,
            direction: str,
            max_members: int
    ) -> str:
        taxi_group = TaxiGroup.create(
            owner_id=owner_id,
            departure_datetime=departure_datetime,
            direction=direction,
            max_members=max_members
        )
        self.taxi_group_repository.save(taxi_group)
        return taxi_group.id

    def delete(self, group_id):
        self.taxi_group_repository.delete(group_id)

    def open(self, group_id: str):
        taxi_group = self.taxi_group_repository.find_by_id(group_id)
        taxi_group.open()
        self.taxi_group_repository.save(taxi_group)

    def close(self, group_id: str):
        taxi_group = self.taxi_group_repository.find_by_id(group_id)
        taxi_group.close()
        self.taxi_group_repository.save(taxi_group)

    def settle(
            self,
            group_id: str,
            fare: int,
            user_costs: list[(str, int)] = None
    ):
        taxi_group = self.taxi_group_repository.find_by_id(group_id)

        billing_policy = AutoBillingPolicy(taxi_group.owner_id)
        if user_costs is not None:
            billing_policy = CustomBillingPolicy(user_costs)

        bills = taxi_group.settle(fare, billing_policy)
        self.taxi_group_repository.save(taxi_group)
        self.bill_repository.save(bills)

    def complete(self, group_id: str):
        taxi_group = self.taxi_group_repository.find_by_id(group_id)
        taxi_group.complete()
        self.taxi_group_repository.save(taxi_group)

    async def participate(self, group_id: str, user_id: str):
        taxi_group = self.taxi_group_repository.find_by_id(group_id)
        taxi_group.participate(user_id)
        await self.chat_group_processor.participate_process(user_id=user_id, group_id=group_id)
        self.taxi_group_repository.save(taxi_group)

    async def leave(self, group_id: str, user_id: str):
        taxi_group = self.taxi_group_repository.find_by_id(group_id)
        taxi_group.leave(user_id)
        await self.chat_group_processor.leave_process(user_id=user_id, group_id=group_id)
        self.taxi_group_repository.save(taxi_group)