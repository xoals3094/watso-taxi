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


class Member:
    def __init__(self, current_member: int, max_member: int, members: List[int]):
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
        return Member(current_member=json['current_member'], max_member=json['max_member'], members=json['members'])


class ResponseGroupDetail:
    def __init__(self,
                 id: str,
                 owner: Owner,
                 direction: str,
                 depart_datetime: datetime,
                 status: str,
                 fee: int,
                 member: Member):
        self.id = id
        self.owner = owner
        self.direction = direction
        self.depart_datetime = depart_datetime
        self.status = status
        self.fee = fee
        self.member = member

    @property
    def json(self):
        return {
            'id': self.id,
            'owner': self.owner.json,
            'direction': self.direction,
            'depart_datetime': self.depart_datetime,
            'status': self.status,
            'fee': self.fee,
            'member': self.member.json,
        }

    @staticmethod
    def mapping(json):
        owner_json = json['owner']
        owner = Owner(id=owner_json['id'], nickname=owner_json['nickname'])

        member_json = json['member']
        member = Member.mapping(member_json)
        return ResponseGroupDetail(id=json['id'],
                                   owner=owner,
                                   direction=json['direction'],
                                   depart_datetime=json['depart_datetime'],
                                   status=json['status'],
                                   fee=json['fee'],
                                   member=member)
