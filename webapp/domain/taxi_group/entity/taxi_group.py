from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from webapp.common.util.id_generator import create_id
from webapp.common.exceptions import domain
from webapp.domain.group.group import Group, Member
from webapp.domain.taxi_group.entity.status import Status
from webapp.domain.taxi_group.entity.direction import Direction


DEFAULT_TAXI_FARE = 6200


class TaxiGroupMember(Member):
    __tablename__ = 'taxi_group_members'

    id = Column(String(32), ForeignKey('members.id'), primary_key=True)
    cost = Column(Integer, nullable=False)


class TaxiGroup(Group):
    __tablename__ = 'taxi_groups'

    id = Column(String(32), ForeignKey('groups.id'), primary_key=True)
    fare = Column(Integer, nullable=False)
    status = Column(String(20), nullable=False)
    departure_datetime = Column(DateTime, nullable=False)
    direction = Column(String(20), nullable=False)

    members = relationship('TaxiGroupMember')

    def _set_status(self, status):
        Status(self.status).to(status)
        self.status = status

    def _adjust(self):
        owner_cost = cost = int(self.fare / len(self.members))
        if self.fare % len(self.members) != 0:
            rest_cost = self.fare % len(self.members)
            owner_cost = cost - (len(self.members) - rest_cost - 1)
            cost = cost + 1

        for member in self.members:
            member.cost = cost
            if self.owner_id == member.id:
                member.cost = owner_cost

    def open(self):
        super(TaxiGroup, self).open()
        self._set_status(Status.OPEN)

    def close(self):
        super(TaxiGroup, self).close()
        self._set_status(Status.CLOSE)

    def settle(self):
        self._set_status(Status.SETTLE)

    def complete(self):
        self._set_status(Status.COMPLETE)

    def participate(self, user_id):
        member = TaxiGroupMember(id=create_id(), group_id=self.id, user_id=user_id)
        super(TaxiGroup, self).participate(member)
        self._adjust()

    def leave(self, user_id):
        super(TaxiGroup, self).leave(user_id)
        self._adjust()

    def set_fare(self, fare: int, members: list[(str, int)]):
        if self.status not in [Status.OPEN, Status.CLOSE]:
            raise domain.InvalidState(msg=f'비용 변경이 불가능한 상태입니다 status={self.status}')

        total_cost = 0
        for user_id, cost in members:
            member = next((member for member in self.members if member.user_id == user_id), None)
            if member is None:
                raise domain.VerifyFail(msg=f'참여자가 일치하지 않습니다 member_id={user_id}')

            member.cost = cost
            total_cost += cost

        if total_cost != fare:
            raise domain.VerifyFail(msg=f'비용이 일치하지 않습니다 total_cost={total_cost} fare={fare}')

        self.fare = fare

    @staticmethod
    def create(
            owner_id: str,
            departure_datetime: datetime,
            direction: str,
            max_members: int
    ):
        return TaxiGroup(
            id=create_id(),
            created_at=datetime.now(),
            owner_id=owner_id,
            is_open=True,
            fare=DEFAULT_TAXI_FARE,
            status=Status.OPEN,
            departure_datetime=departure_datetime,
            direction=Direction(direction),
            max_members=max_members,
            members=[TaxiGroupMember(id=create_id(), user_id=owner_id, cost=DEFAULT_TAXI_FARE)]
        )
