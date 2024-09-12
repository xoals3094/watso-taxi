from abc import *
from webapp.domain.group.group import Group
from webapp.common.database import MySqlDatabase
from webapp.common.schmea import models


class GroupRepository(metaclass=ABCMeta):
    @abstractmethod
    def find_by_id(self, group_id: int) -> Group:
        pass

    @abstractmethod
    def save(self, group: Group):
        pass


class MySQLGroupRepository(MySqlDatabase, GroupRepository, metaclass=ABCMeta):
    def save(self, group: Group):
        group = models.Group(
            id=group.id,
            owner_id=group.owner_id,
            is_open=group.is_open,
            max_members=group.members.max_members
        )
        self.session.add(group)

    def delete(self, group_id):
        pass
