from typing import List
from webapp.common.exceptions import domain


class Bill:
    def __init__(self, user_id: int, cost: int):
        self.user_id = user_id
        self.cost = cost


class Bills:
    @staticmethod
    def verify(bills: list[Bill], fee: int, members: List[int]):
        total_cost = 0
        users = []
        for bill in bills:
            total_cost += bill.cost
            users.append(bill.user_id)

        if fee != total_cost:
            raise domain.VerifyFail(msg=f'정산 비용이 일치하지 않습니다 fee={fee} total_cost={total_cost}')

        for member_id in members:
            if member_id not in users:
                raise domain.VerifyFail(msg=f'정산 유저가 일치하지 않습니다 user_id={member_id}')

    @staticmethod
    def adjust(owner_id: int, fee: int, members: list[int]):
        member_count = len(members)
        owner_cost = cost = int(fee / member_count)
        if fee % len(members) != 0:
            rest_cost = fee % member_count
            owner_cost = cost - (member_count - rest_cost - 1)
            cost = cost + 1

        bills = []
        for member_id in members:
            bill = Bill(user_id=member_id, cost=cost)
            if owner_id == member_id:
                bill.cost = owner_cost

            bills.append(bill)

        return bills
