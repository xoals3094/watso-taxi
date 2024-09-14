import sqlalchemy.exc
from webapp.common.database import MySqlDatabase
from webapp.domain.taxi_group.entity.taxi_group import TaxiGroup
from webapp.common.exceptions import persistence


class TaxiGroupRepository(MySqlDatabase):
    def find_by_id(self, group_id: str) -> TaxiGroup:
        try:
            taxi_group = self.session.query(TaxiGroup).filter(
                TaxiGroup.id == group_id
            ).one()
        except sqlalchemy.exc.NoResultFound:
            raise persistence.ResourceNotFound

        return taxi_group

    def save(self, taxi_group: TaxiGroup):
        self.session.add(taxi_group)
        self.session.commit()
