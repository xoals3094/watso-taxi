import sqlalchemy.exc
from webapp.domain.group.repository import GroupRepository
from webapp.domain.taxi_group.entity.taxi_group import TaxiGroup
from webapp.common.exceptions import persistence


class TaxiGroupRepository(GroupRepository):
    def find_by_id(self, group_id: str) -> TaxiGroup:
        try:
            taxi_group = self.session.query(TaxiGroup).filter(
                TaxiGroup.id == group_id
            ).one()
        except sqlalchemy.exc.NoResultFound:
            raise persistence.ResourceNotFound

        return taxi_group

    def save(self, taxi_group: TaxiGroup):
        for member in taxi_group.members:
            self.session.add(member)
        self.session.add(taxi_group)
        self.session.commit()
