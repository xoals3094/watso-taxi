from datetime import datetime
from bson import ObjectId
from typing import List
from domain.taxi.group.core.status import Status
from exceptions import DomainException, AuthenticationException


class Point:
    def __init__(self, depart_point_id, arrive_point_id):
        self.depart_point_id = depart_point_id
        self.arrive_point_id = arrive_point_id


class Member:
    def __init__(self, max_member: int, members: List[str]):
        self.max_member = max_member
        self.members = members


class Group:
    def __init__(self,
                 id: str,
                 owner_id: str,
                 point: Point,
                 depart_datetime: datetime,
                 status: Status,
                 fee: int,
                 member: Member,
                 notice: str):
        self.id = id
        self.owner_id = owner_id
        self.point = point
        self.depart_datetime = depart_datetime
        self.status = status
        self.fee = fee
        self.member = member
        self.notice = notice

    def modify_notice(self, user_id, notice):
        if self.owner_id != user_id:
            raise AuthenticationException.AccessDeniedException

        if not self.status.modifiable():
            raise DomainException.PostModificationFailedException(
                msg=f"'{self.status}' 상태에서는 게시글의 수정이 불가능합니다."
            )

        self.notice = notice

    def change_status(self, user_id, status):
        if self.owner_id != user_id:
            raise AuthenticationException.AccessDeniedException

        if not self.status.changeable(status):
            raise DomainException.InvalidStateException(
                msg=f"'{self.status}' -> '{status}'는 허용되지 않는 상태코드 변경입니다."
            )

        self.status = status

    def participate(self, user_id):
        if not self.status.can_participate():
            raise DomainException.ParticipationFailedException(
                msg=f"'{self.status}' 상태에서는 참여가 불가능합니다."
            )

        if len(self.member.members) >= self.member.max_member:
            raise DomainException.ParticipationFailedException(
                msg=f"현재 인원이 최대 인원에 도달하여 참여가 불가능합니다. {len(self.member.members)}/{self.member.max_member}"
            )

        if user_id in self.member.members:
            raise DomainException.ParticipationFailedException(
                msg=f"참여가 완료된 사용자입니다."
            )

        self.member.members.append(user_id)

    def leave(self, user_id):
        if self.owner_id == user_id:
            raise DomainException.LeaveFailedException(
                msg=f"대표 유저는 게시글 탈퇴가 불가능합니다."
            )

        if not self.status.can_leave():
            raise DomainException.LeaveFailedException(
                msg=f"'{self.status}' 상태에서는 탈퇴가 불가능합니다."
            )

        if user_id not in self.member.members:
            raise DomainException.LeaveFailedException(
                msg=f"참여하지 않은 사용자입니다."
            )

        self.member.members.remove(user_id)

    @staticmethod
    def create(owner_id: str,
               depart_point_id: str,
               arrive_point_id: str,
               depart_datetime: datetime,
               max_member: int,
               notice: str):
        group = Group(id=str(ObjectId()),
                      owner_id=owner_id,
                      point=Point(depart_point_id, arrive_point_id),
                      depart_datetime=depart_datetime,
                      fee=6200,
                      status=Status.RECRUITING,
                      member=Member(max_member, [owner_id]),
                      notice=notice)

        return group
