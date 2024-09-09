from typing import List


class User:
    def __init__(self, user_id: int, nickname: str):
        self.user_id = user_id
        self.nickname = nickname

    @property
    def json(self):
        return {
            'id': self.user_id,
            'nickname': self.nickname
        }

    @staticmethod
    def mapping(json):
        return User(user_id=json['id'], nickname=json['nickname'])


class Bill:
    def __init__(self, user: User, cost: int):
        self.user = user
        self.cost = cost

    @property
    def json(self):
        return {
            'user': self.user.json,
            'cost': self.cost
        }

    @staticmethod
    def mapping(json):
        return Bill(user=User.mapping(json['user']), cost=json['cost'])


class ResponseBills:
    def __init__(self, fee: int, bills: List[Bill]):
        self.fee = fee
        self.bills = bills

    @property
    def json(self):
        return {
            'fee': self.fee,
            'bills': [bill.json for bill in self.bills]
        }

    @staticmethod
    def mapping(json):
        fee = json['fee']
        bills = [Bill.mapping(bill) for bill in json['bills']]
        return ResponseBills(fee, bills)
