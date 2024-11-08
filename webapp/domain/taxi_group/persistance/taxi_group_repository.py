import sqlalchemy.exc
from sqlalchemy import select
from webapp.domain.group.repository import GroupRepository
from webapp.domain.taxi_group.entity.taxi_group import TaxiGroup
from webapp.common.exceptions import persistence


class TaxiGroupRepository(GroupRepository):
    def find_by_id(self, group_id: str) -> TaxiGroup:
        stmt = select(TaxiGroup).filter_by(id=group_id)
        try:
            taxi_group = self.session.execute(stmt).scalar_one()
        except sqlalchemy.exc.NoResultFound:
            raise persistence.ResourceNotFound

        return taxi_group

    def save(self, taxi_group: TaxiGroup):
        self.session.add(taxi_group)
