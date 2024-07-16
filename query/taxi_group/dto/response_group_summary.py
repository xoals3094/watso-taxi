from datetime import datetime


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
        return Owner(id=str(json['id']), nickname=json['nickname'])


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
                 id: str,
                 owner: Owner,
                 direction: str,
                 depart_datetime: datetime,
                 fee: int,
                 member: Member):
        self.id = id
        self.owner = owner
        self.direction = direction
        self.depart_datetime = depart_datetime
        self.fee = fee
        self.member = member

    @property
    def json(self):
        return {
            'id': self.id,
            'owner': self.owner.json,
            'direction': self.direction,
            'depart_datetime': self.depart_datetime,
            'fee': self.fee,
            'member': self.member.json,
        }

    @staticmethod
    def mapping(json):
        owner = Owner.mapping(json['owner'])
        member = Member.mapping(json['member'])

        return ResponseGroupSummary(id=json['id'],
                                    owner=owner,
                                    direction=json['direction'],
                                    depart_datetime=json['depart_datetime'],
                                    fee=json['fee'],
                                    member=member)
