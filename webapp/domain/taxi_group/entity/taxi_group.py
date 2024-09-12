from datetime import datetime
from typing import List
from webapp.common.util.id_generator import create_id
from webapp.domain.group.group import Group, Member, Members
from webapp.domain.taxi_group.entity.status import Status
from webapp.domain.taxi_group.entity.direction import Direction
from webapp.common.exceptions import domain


DEFAULT_TAXI_FARE = 6200


class TaxiMember(Member):
    def __init__(self, id: int, cost: int):
        super(TaxiMember, self).__init__(id=id)
        self.cost = cost


class TaxiMembers(Members):
    def __init__(self, max_members: int, members: list[TaxiMember]):
        super(TaxiMembers, self).__init__(max_members=max_members, members=members)
        self.members = members

    def adjust(self, owner_id, fare):
        owner_cost = cost = int(fare / len(self.members))
        if fare % len(self.members) != 0:
            rest_cost = fare % len(self.members)
            owner_cost = cost - (len(self.members) - rest_cost - 1)
            cost = cost + 1

        for member in self.members:
            member.cost = cost
            if owner_id == member.id:
                member.cost = owner_cost

    def set_members(self, members: list[TaxiMember]):
        total_cost = 0
        for id, cost in members:
            if id not in self.members:
                raise domain.VerifyFail(
                    msg=f'참여자가 일치하지 않습니다 member_id={id}'
                )

            total_cost += cost

        self.members = members

        return total_cost


class TaxiGroup(Group):
    def __init__(
            self,
            *,
            id: int,
            owner_id: int,
            is_open: bool,
            fare: int,
            status: Status,
            departure_datetime: datetime,
            direction: str,
            members: TaxiMembers
    ):
        super().__init__(
            id=id,
            owner_id=owner_id,
            is_open=is_open,
            members=members
        )
        self.fare = fare
        self.status = status
        self.departure_datetime = departure_datetime
        self.direction = direction
        self.members = members

    def _set_status(self, status):
        self.status.to(status)

    def open(self):
        super(TaxiGroup, self).open()
        self._set_status(Status.OPEN)

    def close(self):
        super(TaxiGroup, self).close()
        self._set_status(Status.CLOSE)

    def settle(self):
        self._set_status(Status.CLOSE)

    def complete(self):
        self._set_status(Status.COMPLETE)

    def participate(self, user_id):
        super(TaxiGroup, self).participate(user_id)
        self.members.adjust(owner_id=self.owner_id, fare=self.fare)

    def leave(self, user_id):
        super(TaxiGroup, self).leave(user_id)
        self.members.adjust(owner_id=self.owner_id, fare=self.fare)

    def set_fare(self, fare: int, members: list[TaxiMember]):
        if self.status not in [Status.OPEN, Status.CLOSE]:
            raise domain.InvalidState(msg=f'비용 변경이 불가능한 상태입니다 status={self.status}')

        total_cost = self.members.set_members(members=members)
        if total_cost != fare:
            raise domain.VerifyFail(
                msg=f'비용이 일치하지 않습니다 total_cost={total_cost} fare={fare}'
            )

        self.fare = fare

    @staticmethod
    def create(
            owner_id: int,
            departure_datetime: datetime,
            direction: str,
            max_members: int
    ):
        taxi_member = TaxiMember(id=owner_id, cost=DEFAULT_TAXI_FARE)
        taxi_members = TaxiMembers(max_members=max_members, members=[taxi_member])
        return TaxiGroup(
            id=create_id(),
            owner_id=owner_id,
            is_open=True,
            fare=DEFAULT_TAXI_FARE,
            status=Status.OPEN,
            departure_datetime=departure_datetime,
            direction=Direction(direction),
            members=taxi_members
        )
