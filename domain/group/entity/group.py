from util.id_generator import create_id
from typing import List
from exceptions import DomainException


class Member:
    def __init__(self, max_member: int, members: List[int]):
        self.max_member = max_member
        self.members = members

    def add(self, user_id):
        if self.max_member <= len(self.members):
            raise DomainException.ParticipationFailedException(msg=f'최대 인원에 도달하여 참여 불가능합니다 {len(self.members)}/{self.max_member}')

        if user_id in self.members:
            raise DomainException.ParticipationFailedException(msg='이미 참여한 유저입니다')

        self.members.append(user_id)

    def remove(self, user_id):
        if user_id not in self.members:
            raise DomainException.LeaveFailedException(msg='참여하지 않은 유저입니다')

        self.members.remove(user_id)

    @staticmethod
    def mapping(json):
        return Member(max_member=json['max_member'], members=json['members'])


class Group:
    def __init__(self, id: int, owner_id: int, is_open: bool, member: Member):
        self.id = id
        self.owner_id = owner_id
        self.is_open = is_open
        self.member = member

    def open(self):
        self.is_open = True

    def close(self):
        self.is_open = False

    def participate(self, user_id):
        if self.is_open is False:
            raise DomainException.ParticipationFailedException(msg=f'참여가 불가능한 그룹입니다 is_open={self.is_open}')

        self.member.add(user_id)

    def leave(self, user_id):
        if self.owner_id == user_id:
            raise DomainException.ParticipationFailedException(msg=f'그룹장 유저는 탈퇴가 불가능합니다')

        if self.is_open is False:
            raise DomainException.ParticipationFailedException(msg=f'탈퇴가 불가능한 그룹입니다 is_open={self.is_open}')

        self.member.remove(user_id)

    def verify_users(self, users: List[int]):
        for member_id in self.member.members:
            if member_id not in users:
                raise DomainException.VerifyFailException(
                    msg=f'참여자가 일치하지 않습니다 member_id={member_id} users={users}'
                )

    @staticmethod
    def create(owner_id: int, max_member: int):
        group_id = create_id()
        member = Member(max_member, [owner_id])
        group = Group(id=group_id, owner_id=owner_id, is_open=True, member=member)

        return group

    @staticmethod
    def mapping(json):
        return Group(id=json['id'],
                     owner_id=json['owner_id'],
                     is_open=json['is_open'],
                     member=Member.mapping(json['member']))
