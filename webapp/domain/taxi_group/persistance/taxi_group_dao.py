import sqlalchemy
from sqlalchemy.orm import joinedload
from sqlalchemy import select, or_, case, func
from datetime import datetime, timedelta
from webapp.common.exceptions import persistence
from webapp.domain.user.entity.user import User
from webapp.domain.group.group import Group, Member
from webapp.domain.taxi_group.persistance.taxi_group_repository import TaxiGroupRepository
from webapp.domain.taxi_group.entity.bill import Bill, Charge
from webapp.domain.taxi_group.entity.taxi_group import TaxiGroup
from webapp.domain.taxi_group.entity.status import Status


class TaxiGroupDao(TaxiGroupRepository):
    def __init__(self, session):
        super(TaxiGroupDao, self).__init__(session)

    def find_taxi_group_detail_by_id(self, user_id: str, group_id: str) -> TaxiGroup:
        current_member = select(Member.group_id, func.count()).group_by(Member.group_id).cte("current_member")
        is_member = select(Member.user_id).filter(Member.group_id == group_id).filter(Member.user_id == user_id).exists()

        stmt = select(
            TaxiGroup.id,
            case(
                (TaxiGroup.owner_id == user_id, "OWNER"),
                (is_member, "MEMBER"),
                else_="NON_MEMBER"
            ),
            current_member.c.count,
            TaxiGroup.max_members,
            TaxiGroup.status,
            TaxiGroup.departure_datetime,
            TaxiGroup.direction,
            Bill.fee,
            Charge.cost
        ).join(
            current_member
        ).outerjoin_from(
            TaxiGroup, Bill
        ).outerjoin_from(
            Bill, Charge
        ).filter(
            TaxiGroup.id == group_id
        ).filter(
            or_(Bill.id == None, Charge.user_id == user_id)
        )

        try:
            taxi_group = self.session.execute(stmt).one()
        except sqlalchemy.exc.NoResultFound:
            raise persistence.ResourceNotFound

        return taxi_group

    def find_complete(self, user_id: str):
        my_groups_subquery = select(Member.group_id).filter_by(user_id=user_id).subquery()
        current_member = select(Member.group_id, func.count()).group_by(Member.group_id).cte("current_member")

        stmt = select(
            TaxiGroup.id,
            current_member.c.count,
            TaxiGroup.max_members,
            TaxiGroup.status,
            TaxiGroup.departure_datetime,
            TaxiGroup.direction,
            Bill.fee,
            Charge.cost
        ).join(
            current_member
        ).join_from(
            TaxiGroup, Bill
        ).join_from(
            Bill, Charge
        ).filter(
            Charge.user_id == user_id
        ).filter(
            TaxiGroup.status == Status.COMPLETE
        ).filter(
            TaxiGroup.departure_datetime >= datetime.now() - timedelta(days=90)
        ).filter(
            Group.id.in_(my_groups_subquery.select())
        ).order_by(TaxiGroup.departure_datetime)

        taxi_groups = self.session.execute(stmt).all()

        return taxi_groups

    def find_joined(self, user_id: str, departure_datetime: datetime):
        my_groups_subquery = select(Member.group_id).filter_by(user_id=user_id).subquery()
        current_member = select(Member.group_id, func.count()).group_by(Member.group_id).cte("current_member")

        stmt = select(
            TaxiGroup.id,
            current_member.c.count,
            TaxiGroup.max_members,
            TaxiGroup.status,
            TaxiGroup.departure_datetime,
            TaxiGroup.direction,
            Bill.fee,
            Charge.cost
        ).filter(
            TaxiGroup.status != Status.COMPLETE
        ).filter(
            TaxiGroup.departure_datetime >= departure_datetime
        ).filter(
            Group.id.in_(my_groups_subquery.select())
        ).filter(
            or_(Bill.id == None, Charge.user_id == user_id)
        ).join(
            current_member
        ).outerjoin_from(
            TaxiGroup, Bill
        ).outerjoin_from(
            Bill, Charge
        ).order_by(TaxiGroup.departure_datetime)
        taxi_groups = self.session.execute(stmt).all()
        return taxi_groups

    def find_joinable(self, user_id, direction, departure_datetime):
        my_groups_subquery = select(Member.group_id).filter_by(user_id=user_id).subquery()
        current_member = select(Member.group_id, func.count()).group_by(Member.group_id).cte("current_member")

        stmt = select(
            TaxiGroup.id,
            current_member.c.count,
            TaxiGroup.max_members,
            TaxiGroup.status,
            TaxiGroup.departure_datetime,
            TaxiGroup.direction,
        ).filter(
            TaxiGroup.status == Status.OPEN
        ).filter(
            TaxiGroup.direction == direction
        ).filter(
            TaxiGroup.departure_datetime >= departure_datetime
        ).filter(
            Group.id.not_in(my_groups_subquery.select())
        ).join(
            current_member
        ).order_by(TaxiGroup.departure_datetime)

        taxi_groups = self.session.execute(stmt).all()
        return taxi_groups

    def find_fare(self, group_id: str):
        stmt = select(Bill).where(
            Bill.group_id == group_id
        )
        bill = self.session.execute(stmt).scalars().first()
        fare = bill.fee

        stmt = select(
            Charge.user_id,
            User.nickname,
            Charge.cost
        ).join(User).where(Charge.bill_id == bill.id)

        members = tuple(self.session.execute(stmt))
        return fare, members
