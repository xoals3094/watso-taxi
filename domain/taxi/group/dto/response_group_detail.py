# review
from datetime import datetime
from typing import List


class Owner:
    def __init__(self, id: str, nickname: str):
        self.id = id
        self.nickname = nickname

    @property
    def json(self):
        return {
            'id': self.id,
            'nickname': self.nickname
        }

    @staticmethod
    def mapping(json):
        return Owner(id=str(json['_id']), nickname=json['nickname'])


class Point:
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name

    @property
    def json(self):
        return {
            'id': self.id,
            'name': self.name
        }

    @staticmethod
    def mapping(json):
        return Point(id=str(json['_id']), name=json['name'])


class Points:
    def __init__(self, depart_point: Point, arrive_point: Point):
        self.depart_point = depart_point
        self.arrive_point = arrive_point

    @property
    def json(self):
        return {
            'depart_point': self.depart_point.json,
            'arrive_point': self.arrive_point.json
        }

    @staticmethod
    def mapping(json):
        depart_point = Point.mapping(json['depart_point'])
        arrive_point = Point.mapping(json['arrive_point'])
        return Points(depart_point=depart_point, arrive_point=arrive_point)


class Member:
    def __init__(self, current_member: int, max_member: int, members: List[str]):
        self.current_member = current_member
        self.max_member = max_member
        self.members = members

    @property
    def json(self):
        return {
            'current_member': self.current_member,
            'max_member': self.max_member,
            'members': self.members
        }

    @staticmethod
    def mapping(json):
        members = [str(member) for member in json['members']]
        return Member(current_member=len(json['members']), max_member=json['max_member'], members=members)


class ResponseGroupDetail:
    def __init__(self,
                 id: str,
                 owner: Owner,
                 point: Points,
                 depart_datetime: datetime,
                 status: str,
                 fee: int,
                 member: Member,
                 notice: str):
        self.id = id
        self.owner = owner
        self.point = point
        self.depart_datetime = depart_datetime
        self.status = status
        self.fee = fee
        self.member = member
        self.notice = notice

    @property
    def json(self):
        return {
            'id': self.id,
            'owner': self.owner.json,
            'point': self.point.json,
            'depart_datetime': self.depart_datetime,
            'status': self.status,
            'fee': self.fee,
            'member': self.member.json,
            'notice': self.notice
        }

    @staticmethod
    def mapping(post_json):
        owner_json = post_json['owner']
        owner = Owner.mapping(owner_json)

        point_json = post_json['point']
        point = Points.mapping(point_json)

        member_json = post_json['member']
        member = Member.mapping(member_json)

        return ResponseGroupDetail(id=str(post_json['_id']),
                                   owner=owner,
                                   point=point,
                                   depart_datetime=post_json['depart_datetime'],
                                   status=post_json['status'],
                                   fee=post_json['fee'],
                                   member=member,
                                   notice=post_json['notice'])


