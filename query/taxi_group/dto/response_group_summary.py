from datetime import datetime
from domain.taxi_group.entity.status import Status


class Member:
    def __init__(self, current_member: int, max_member: int):
        self.current_member = current_member
        self.max_member = max_member

    @property
    def json(self):
        return {
            'current_member': self.current_member,
            'max_member': self.max_member
        }

    @staticmethod
    def mapping(json):
        return Member(current_member=json['current_member'], max_member=json['max_member'])


class ResponseGroupSummary:
    def __init__(self,
                 id: int,
                 owner_id: int,
                 direction: str,
                 status: Status,
                 depart_datetime: datetime,
                 fee: int,
                 member: Member):
        self.id = id
        self.owner_id = owner_id
        self.direction = direction
        self.status = status
        self.depart_datetime = depart_datetime
        self.fee = fee
        self.member = member

    @property
    def json(self):
        return {
            'id': self.id,
            'owner_id': self.owner_id,
            'direction': self.direction,
            'status': self.status,
            'depart_datetime': self.depart_datetime,
            'fee': self.fee,
            'member': self.member.json,
        }

    @staticmethod
    def mapping(json):
        member = Member.mapping(json['member'])

        return ResponseGroupSummary(id=json['id'],
                                    owner_id=json['owner_id'],
                                    direction=json['direction'],
                                    status=json['status'],
                                    depart_datetime=json['depart_datetime'],
                                    fee=json['fee'],
                                    member=member)
