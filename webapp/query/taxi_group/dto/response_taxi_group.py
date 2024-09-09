from datetime import datetime


class Member:
    def __init__(self, current_member: int, max_member: int):
        self.current_member = current_member
        self.max_member = max_member

    @property
    def json(self):
        return {
            'current_member': self.current_member,
            'max_member': self.max_member,
        }

    @staticmethod
    def mapping(json):
        return Member(current_member=json['current_member'], max_member=json['max_member'])


class Fee:
    def __init__(self, total, cost):
        self.total = total
        self.cost = cost

    @property
    def json(self):
        return {
            'total': self.total,
            'cost': self.cost
        }

    @staticmethod
    def mapping(json):
        return Fee(total=json['total'], cost=json['cost'])


class ResponseTaxiGroup:
    def __init__(self,
                 id: str,
                 owner_id: int,
                 direction: str,
                 depart_datetime: datetime,
                 status: str,
                 fee: Fee,
                 member: Member):
        self.id = id
        self.owner_id = owner_id
        self.direction = direction
        self.depart_datetime = depart_datetime
        self.status = status
        self.fee = fee
        self.member = member

    def get_json_detail(self, user_id):
        json = self.json
        json['role'] = 'OWNER' if user_id == self.owner_id else 'NORMAL'
        return json

    @property
    def json(self):
        return {
            'id': self.id,
            'direction': self.direction,
            'depart_datetime': self.depart_datetime,
            'status': self.status,
            'fee': self.fee.json,
            'member': self.member.json,
        }

    @staticmethod
    def mapping(json):
        member = Member.mapping(json['member'])
        fee = Fee.mapping(json['fee'])
        return ResponseTaxiGroup(id=json['id'],
                                 owner_id=json['owner_id'],
                                 direction=json['direction'],
                                 depart_datetime=json['depart_datetime'],
                                 status=json['status'],
                                 fee=fee,
                                 member=member)
