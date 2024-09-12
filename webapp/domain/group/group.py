from abc import *
from typing import List
from webapp.common.exceptions import domain


class Member(metaclass=ABCMeta):
    def __init__(self, id: int):
        self.id = id


class Members(metaclass=ABCMeta):
    def __init__(
            self,
            max_members: int,
            members: List[Member]
    ):
        self.max_members = max_members
        self.members = members

    def __contains__(self, id: int):
        for member in self.members:
            if member.id == id:
                return True

        return False

    def add(self, user_id):
        if self.max_members <= len(self.members):
            raise domain.ParticipationFailed(msg=f'최대 인원에 도달하여 참여 불가능합니다 {len(self.members)}/{self.max_members}')

        if user_id in self.members:
            raise domain.ParticipationFailed(msg='이미 참여한 유저입니다')

        self.members.append(user_id)

    def remove(self, user_id):
        if user_id not in self.members:
            raise domain.LeaveFailed(msg='참여하지 않은 유저입니다')

        self.members.remove(user_id)


class Group(metaclass=ABCMeta):
    def __init__(
            self,
            id: int,
            owner_id: int,
            is_open: bool,
            members: Members
    ):
        self.id = id
        self.owner_id = owner_id
        self.is_open = is_open
        self.members = members

    def open(self):
        self.is_open = True

    def close(self):
        self.is_open = False

    def participate(self, user_id):
        if self.owner_id == user_id:
            raise domain.ParticipationFailed(msg=f'그룹장 유저는 참여가 불가능합니다')

        if self.is_open is False:
            raise domain.ParticipationFailed(msg=f'참여가 마감된 그룹입니다 is_open={self.is_open}')

        self.members.add(user_id)

    def leave(self, user_id):
        if self.owner_id == user_id:
            raise domain.ParticipationFailed(msg=f'그룹장 유저는 탈퇴가 불가능합니다')

        if self.is_open is False:
            raise domain.ParticipationFailed(msg=f'탈퇴가 불가능한 그룹입니다 is_open={self.is_open}')

        self.members.remove(user_id)
