from domain.group.entity.group import Group
from domain.group.application.group_repository import GroupRepository


class GroupService:
    def __init__(self, group_repository: GroupRepository):
        self.group_repository = group_repository

    def owner_permission(self, group_id, user_id):
        group = self.group_repository.find_group_by_id(group_id)
        group.check_owner_permission(user_id)

    def create(self, owner_id: int, max_member: int) -> int:
        group = Group.create(owner_id=owner_id, max_member=max_member)
        self.group_repository.save(group)
        return group.id

    def delete(self, group_id):
        group = self.group_repository.find_group_by_id(group_id)
        self.group_repository.delete(group.id)

    def open(self, group_id):
        group = self.group_repository.find_group_by_id(group_id)
        group.open()
        self.group_repository.save(group)

    def close(self, group_id):
        group = self.group_repository.find_group_by_id(group_id)
        group.close()
        self.group_repository.save(group)

    def participate(self, group_id, user_id):
        group = self.group_repository.find_group_by_id(group_id)
        group.participate(user_id)

    def leave(self, user_id, group_id):
        group = self.group_repository.find_group_by_id(group_id)
        group.leave(user_id)
