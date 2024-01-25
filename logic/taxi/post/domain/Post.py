from datetime import datetime
from bson import ObjectId
from typing import List
from .Status import Status


class Owner:
    def __init__(self, id, name):
        self.id = id
        self.name = name


class Point:
    def __init__(self, depart_point_id, arrive_point_id):
        self.depart_point_id = depart_point_id
        self.arrive_point_id = arrive_point_id


class Member:
    def __init__(self, max_member: int, members: List[str]):
        self.max_member = max_member
        self.members = members


class Post:
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

    def modify(self, notice):
        self.notice = notice

    def change_status(self, status):
        self.status = status

    def join(self, user_id):
        self.member.members.append(user_id)

    def quit(self, user_id):
        self.member.members.remove(user_id)

    @staticmethod
    def create(owner_id: str,
               depart_point_id: str,
               arrive_point_id: str,
               depart_datetime: datetime,
               max_member: int,
               notice: str):
        post = Post(id=str(ObjectId()),
                    owner_id=owner_id,
                    point=Point(depart_point_id, arrive_point_id),
                    depart_datetime=depart_datetime,
                    fee=6200,
                    status=Status.RECRUITING,
                    member=Member(max_member, [owner_id]),
                    notice=notice)

        return post
