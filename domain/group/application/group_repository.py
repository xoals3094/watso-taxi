from abc import *
from domain.group.entity.group import Group


class GroupRepository(metaclass=ABCMeta):
    @abstractmethod
    def find_group_by_id(self, group_id) -> Group:
        pass

    @abstractmethod
    def save(self, group: Group):
        pass

    @abstractmethod
    def update_is_open(self, group_id, is_open: bool):
        pass

    @abstractmethod
    def append_member(self, group_id: int, user_id: int):
        pass

    @abstractmethod
    def delete_member(self, group_id: int, user_id: int):
        pass

    @abstractmethod
    def delete(self, group_id):
        pass
