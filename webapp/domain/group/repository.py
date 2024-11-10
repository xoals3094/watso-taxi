from abc import *
from sqlalchemy import delete
from webapp.common.database import MySqlDatabase
from webapp.domain.group.group import Group


class GroupRepository(MySqlDatabase, metaclass=ABCMeta):
    @abstractmethod
    def find_by_id(self, group_id) -> Group:
        pass

    def save(self, group: Group):
        self.session.add(group)

    def delete(self, group_id):
        stmt = delete(Group).filter_by(id=group_id)
        self.session.execute(stmt)
        self.session.commit()
