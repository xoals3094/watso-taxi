from datetime import datetime
from typing import List


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
                 owner_id: int,
                 direction: str,
                 depart_datetime: datetime,
                 status: str,
                 fee: int,
                 member: Member):
        self.id = id
        self.owner_id = owner_id
        self.direction = direction
        self.depart_datetime = depart_datetime
        self.status = status
        self.fee = fee
        self.member = member

    @property
    def json(self):
        return {
            'id': self.id,
            'owner_id': self.owner_id,
            'direction': self.direction,
            'depart_datetime': self.depart_datetime,
            'status': self.status,
            'fee': self.fee,
            'member': self.member.json,
        }

    @staticmethod
    def mapping(json):
        member_json = json['member']
        member = Member.mapping(member_json)
        return ResponseGroupDetail(id=json['id'],
                                   owner_id=json['owner_id'],
                                   direction=json['direction'],
                                   depart_datetime=json['depart_datetime'],
                                   status=json['status'],
                                   fee=json['fee'],
                                   member=member)
