from datetime import datetime

from domain.taxi.group.persistance.group_update_dao import MongoDBGroupUpdateDao
from domain.taxi.group.entity.group import Group
from domain.taxi.group.core.status import Status

from abc import *


class GroupRepository(metaclass=ABCMeta):
    @abstractmethod
    def find_group_by_id(self, group_id) -> Group:
        pass

    @abstractmethod
    def save(self, group: Group):
        pass

    @abstractmethod
    def delete(self, group_id):
        pass


class GroupService:
    def __init__(self, group_repository: GroupRepository, group_update_dao: MongoDBGroupUpdateDao):
        self.group_repository = group_repository
        self.group_update_dao = group_update_dao

    def create(self,
               owner_id: str,
               depart_point_id: str,
               arrive_point_id: str,
               depart_datetime: datetime,
               max_member: int,
               notice: str) -> str:
        group = Group.create(owner_id=owner_id,
                             depart_point_id=depart_point_id,
                             arrive_point_id=arrive_point_id,
                             depart_datetime=depart_datetime,
                             max_member=max_member,
                             notice=notice)
        self.group_repository.save(group)
        return group.id

    def delete(self, post_id, user_id):
        group = self.group_repository.find_group_by_id(post_id)
        self.group_repository.delete(group.id)

    def modify_notice(self, user_id: str, group_id: str, notice: str):
        group = self.group_repository.find_group_by_id(group_id)
        group.modify_notice(user_id=user_id, notice=notice)
        self.group_update_dao.update_notice(group_id=group.id, notice=group.notice)

    def change_status(self, user_id: str, group_id: str, status: Status):
        group = self.group_repository.find_group_by_id(group_id)
        group.change_status(user_id=user_id, status=status)
        self.group_update_dao.update_status(group_id=group.id, status=group.status)

    def participate(self, user_id, group_id):
        group = self.group_repository.find_group_by_id(group_id)
        group.participate(user_id)
        self.group_update_dao.update_members(group_id=group.id, members=group.member.members)

    def leave(self, user_id, group_id):
        group = self.group_repository.find_group_by_id(group_id)
        group.leave(user_id)
        self.group_update_dao.update_members(group_id=group.id, members=group.member.members)
