from multipledispatch import dispatch
from datetime import datetime

from domain.group.application.group_service import GroupService
from domain.group.application.group_repository import GroupRepository
from domain.taxi_group.core.status import Status
from domain.taxi_group.entity.taxi_group import TaxiGroup
from domain.taxi_group.persistance.mysql_taxi_group_dao import MySQLTaxiGroupDao


class TaxiGroupService(GroupService):
    def __init__(self, group_repository: GroupRepository, taxi_group_dao: MySQLTaxiGroupDao):
        super().__init__(group_repository=group_repository)
        self.group_repository = group_repository
        self.taxi_group_dao = taxi_group_dao

    @dispatch(int, int, datetime, int, int)
    def create(self,
               owner_id: int,
               max_member: int,
               depart_datetime: datetime,
               depart_location_id: int,
               arrive_location_id: int) -> int:
        group_id = super().create(owner_id, max_member)
        taxi_group = TaxiGroup.create(group_id=group_id,
                                      depart_datetime=depart_datetime,
                                      depart_location_id=depart_location_id,
                                      arrive_location_id=arrive_location_id)
        self.taxi_group_dao.insert(taxi_group)

        return group_id

    def settle(self, group_id: str):
        current_status = self.taxi_group_dao.find_status_by_id(group_id)

        next_status = Status.SETTLEMENT
        current_status.to(next_status)

        # 정산 코드
        super().close(group_id)
        self.taxi_group_dao.update_status(next_status)

    def complete(self, group_id: str):
        current_status = self.taxi_group_dao.find_status_by_id(group_id)

        next_status = Status.COMPLETED
        current_status.to(Status.COMPLETED)

        # 완료 코드
        self.taxi_group_dao.update_status(next_status)

