from abc import *
from webapp.common.database import MySqlDatabase
from webapp.domain.group.group import Group


class GroupRepository(MySqlDatabase, metaclass=ABCMeta):
    @abstractmethod
    def find_by_id(self, group_id) -> Group:
        pass

    @abstractmethod
    def save(self, group: Group):
        pass

    def delete(self, group_id):
        group = self.session.query(Group).filter(Group.id == group_id).one()
        self.session.delete(group)
        self.session.commit()
