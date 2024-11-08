from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey

from webapp.domain.group.group import Group
from webapp.domain.taxi_group.entity.status import Status
from webapp.domain.taxi_group.entity.direction import Direction
from webapp.domain.taxi_group.entity.bill import Bill
from webapp.domain.taxi_group.entity.billing_policy import BillingPolicy


class TaxiGroup(Group):
    __tablename__ = 'taxi_groups'

    id = Column(String(32), ForeignKey('groups.id', ondelete='CASCADE'), primary_key=True)
    status = Column(String(20), nullable=False)
    departure_datetime = Column(DateTime, nullable=False)
    direction = Column(String(20), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'taxi',
    }

    def _set_status(self, status):
        Status(self.status).to(status)
        self.status = status

    def open(self):
        super(TaxiGroup, self).open()
        self._set_status(Status.OPEN)

    def close(self):
        super(TaxiGroup, self).close()
        self._set_status(Status.CLOSE)

    def settle(self, fare: int, billing_policy: BillingPolicy) -> list[Bill]:
        self._set_status(Status.SETTLE)
        bills = billing_policy.create_bills(fare, self.members)
        return bills

    def complete(self):
        self._set_status(Status.COMPLETE)

    @staticmethod
    def create(
            owner_id: str,
            departure_datetime: datetime,
            direction: str,
            max_members: int
    ):
        return Group._create(
            TaxiGroup,
            owner_id,
            status=Status.OPEN,
            departure_datetime=departure_datetime,
            direction=Direction(direction),
            max_members=max_members,
        )
