from domain.group.entity.group import Group
from domain.group.persistance.group_repository import MySQLGroupRepository


class GroupService:
    def __init__(self, group_repository: MySQLGroupRepository):
        self.group_repository = group_repository

    def create(self, owner_id: int, max_member: int) -> int:
        group = Group.create(owner_id=owner_id, max_member=max_member)
        self.group_repository.save(group)
        return group.id

    def delete(self, group_id: int):
        group = self.group_repository.find_group_by_id(group_id)
        self.group_repository.delete(group.id)

    def open(self, group_id: int):
        group = self.group_repository.find_group_by_id(group_id)
        group.open()
        self.group_repository.update_is_open(group.id, group.is_open)

    def close(self, group_id: int):
        group = self.group_repository.find_group_by_id(group_id)
        group.close()
        self.group_repository.update_is_open(group.id, group.is_open)

    def participate(self, group_id: int, user_id: int):
        group = self.group_repository.find_group_by_id(group_id)
        group.participate(user_id)
        self.group_repository.append_member(group_id, user_id)

    def leave(self, group_id: int, user_id: int):
        group = self.group_repository.find_group_by_id(group_id)
        group.leave(user_id)
        self.group_repository.delete_member(group_id, user_id)
