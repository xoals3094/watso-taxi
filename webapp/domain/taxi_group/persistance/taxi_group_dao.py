from sqlalchemy.orm import joinedload
from sqlalchemy import select
from datetime import datetime, timedelta
from webapp.domain.taxi_group.persistance.taxi_group_repository import TaxiGroupRepository
from webapp.domain.taxi_group.entity.taxi_group import Group, TaxiGroup
from webapp.domain.taxi_group.entity.taxi_group import Member, TaxiGroupMember
from webapp.domain.taxi_group.entity.status import Status


class TaxiGroupDao(TaxiGroupRepository):
    def __init__(self, session):
        super(TaxiGroupDao, self).__init__(session)

    def find_complete(self, user_id: str) -> list[TaxiGroup]:
        my_groups_subquery = select(Member.group_id).filter_by(user_id=user_id).subquery()

        stmt = select(
            TaxiGroup
        ).options(
            joinedload(TaxiGroup.members)
        ).filter(
            TaxiGroup.status == Status.COMPLETE
        ).filter(
            TaxiGroup.departure_datetime >= datetime.now() - timedelta(days=90)
        ).filter(
            Group.id.in_(my_groups_subquery.select())
        ).order_by(TaxiGroup.departure_datetime).all()

        taxi_groups = self.session.execute(stmt).scalars().unique().all()

        return taxi_groups

    def find_joined(self, user_id: str, departure_datetime: datetime) -> list[TaxiGroup]:
        my_groups_subquery = select(Member.group_id).filter_by(user_id=user_id).subquery()

        stmt = select(
            TaxiGroup
        ).options(
            joinedload(TaxiGroup.members)
        ).filter(
            TaxiGroup.status != Status.COMPLETE
        ).filter(
            TaxiGroup.departure_datetime >= departure_datetime
        ).filter(
            Group.id.in_(my_groups_subquery.select())
        ).order_by(TaxiGroup.departure_datetime)

        taxi_groups = self.session.execute(stmt).scalars().unique().all()

        return taxi_groups

    def find_joinable(self, user_id, direction, departure_datetime) -> list[TaxiGroup]:
        my_groups_subquery = select(Member.group_id).filter_by(user_id=user_id).subquery()

        stmt = select(
            TaxiGroup
        ).options(
            joinedload(TaxiGroup.members)
        ).filter(
            TaxiGroup.status == Status.OPEN
        ).filter(
            TaxiGroup.direction == direction
        ).filter(
            TaxiGroup.departure_datetime >= departure_datetime
        ).filter(
            Group.id.not_in(my_groups_subquery.select())
        ).order_by(TaxiGroup.departure_datetime)

        taxi_groups = self.session.execute(stmt).scalars().unique().all()

        return taxi_groups

    def find_fare(self, group_id: str):
        stmt = select(TaxiGroup.fare).where(TaxiGroup.id == group_id)
        result = self.session.execute(stmt)
        fare = result.scalar_one()

        stmt = select(
            TaxiGroupMember.user_id,
            TaxiGroupMember.user.nickname,
            TaxiGroupMember.cost
        ).join(
            TaxiGroupMember.user
        ).where(
            TaxiGroupMember.group_id == group_id
        )
        members = self.session.execute(stmt)

        return fare, tuple(members)
