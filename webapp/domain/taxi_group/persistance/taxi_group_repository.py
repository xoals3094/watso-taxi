from abc import *
from webapp.domain.group.repository import MySQLGroupRepository
from webapp.domain.taxi_group.entity.taxi_group import TaxiGroup, TaxiMember, TaxiMembers
from webapp.domain.taxi_group.entity.status import Status
from webapp.domain.taxi_group.entity.direction import Direction
from webapp.common.schmea import models


class TaxiGroupRepository(MySQLGroupRepository, metaclass=ABCMeta):
    @abstractmethod
    def find_by_id(self, group_id) -> TaxiGroup:
        pass


class MySQLTaxiGroupRepository(TaxiGroupRepository):
    def find_by_id(self, group_id) -> TaxiGroup:
        taxi_group_members = self.session.query(model.TaxiGroupMember).filter(
            model.TaxiGroupMember.group_id == group_id
        ).all()

        taxi_group = self.session.query(model.TaxiGroup).get(
            model.TaxiGroup.group_id == group_id
        )

        taxi_group_members = TaxiMembers(
            max_members=taxi_group.fare,
            members=[
                TaxiMember(id=taxi_group_member.id, cost=taxi_group_member)
                for taxi_group_member in taxi_group_members
            ]
        )

        return TaxiGroup(
            id=taxi_group.id,
            owner_id=taxi_group.owner_id,
            is_open=taxi_group.is_open,
            fare=taxi_group.fare,
            status=Status(taxi_group.status),
            departure_datetime=taxi_group.departure_datetime,
            direction=Direction(taxi_group.direction),
            members=taxi_group_members,
        )

    def save(self, taxi_group: TaxiGroup):
        super(MySQLTaxiGroupRepository, self).save(taxi_group)
        taxi_group = models.TaxiGroup(
            group_id=taxi_group.id,
            fare=taxi_group.fare,
            status=taxi_group.status,
            departure_datetime=taxi_group.departure_datetime,
            direction=taxi_group.direction
        )

        self.session.add(taxi_group)
        self.session.commit()
