from datetime import datetime
from webapp.domain.taxi_group.entity.taxi_group import TaxiGroup
from webapp.domain.chat.chat_group_processor import ChatGroupProcessor
from webapp.domain.taxi_group.persistance.taxi_group_repository import TaxiGroupRepository


class TaxiGroupService:
    def __init__(
            self,
            chat_group_processor: ChatGroupProcessor,
            taxi_group_repository: TaxiGroupRepository
    ):
        self.chat_group_processor = chat_group_processor
        self.taxi_group_repository = taxi_group_repository

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

    def settle(self, group_id: str):
        taxi_group = self.taxi_group_repository.find_by_id(group_id)
        taxi_group.settle()
        self.taxi_group_repository.save(taxi_group)

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

    def update_fare(
            self,
            group_id: str,
            fare: int,
            members: list[(str, int)]
    ):
        taxi_group = self.taxi_group_repository.find_by_id(group_id)
        taxi_group.set_fare(fare, members)
        self.taxi_group_repository.save(taxi_group)
