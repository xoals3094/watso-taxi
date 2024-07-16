from typing import List
from exceptions import domain


class Bill:
    def __init__(self, user_id: int, cost: int):
        self.user_id = user_id
        self.cost = cost


class Bills:
    def __init__(self, bills: List[Bill]):
        self.bills = bills

    def verify(self, fee: int, members: List[int]):
        total_cost = 0
        users = []
        for bill in self.bills:
            total_cost += bill.cost
            users.append(bill.user_id)

        if fee != total_cost:
            raise domain.VerifyFail(msg=f'정산 비용이 일치하지 않습니다 fee={fee} total_cost={total_cost}')

        for member_id in members:
            if member_id not in users:
                raise domain.VerifyFail(msg=f'정산 유저가 일치하지 않습니다 user_id={member_id}')

    def divide(self, owner_id: int, fee):
        user_count = len(self.bills)
        divided_cost = int(fee / user_count)

        for bill in self.bills:
            bill.cost = divided_cost

        if fee % user_count != 0:
            rest_cost = fee % user_count

            owner_cost = divided_cost - (user_count - rest_cost - 1)
            user_cost = divided_cost + 1

            for bill in self.bills:
                bill.cost = user_cost
                if bill.user_id == owner_id:
                    bill.cost = owner_cost
