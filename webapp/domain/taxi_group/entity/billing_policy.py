from abc import *
from webapp.common.exceptions import domain
from webapp.common.util.id_generator import create_id
from webapp.domain.taxi_group.entity.bill import Bill, Charge


class BillingPolicy(metaclass=ABCMeta):
    @abstractmethod
    def create_bills(self, group_id: str, fare: int, members: list[str]) -> Bill:
        pass


class AutoBillingPolicy(BillingPolicy):
    def __init__(self, owner_id: str):
        self.owner_id = owner_id

    def create_bills(self, group_id: str, fare: int, members: list[str]) -> Bill:
        cost = owner_cost = int(fare / len(members))
        if fare % len(members) != 0:
            rest_cost = fare % len(members)
            owner_cost = cost - (len(members) - rest_cost - 1)
            cost = cost + 1

        return Bill(
            id=create_id(),
            group_id=group_id,
            fee=fare,
            charges=[
                Charge(
                    id=create_id(),
                    user_id=member_id,
                    cost=owner_cost if member_id == self.owner_id else cost
                ) for member_id in members
            ]
        )


class CustomBillingPolicy(BillingPolicy):
    def __init__(self, member_costs: list[str, int]):
        self.member_costs = member_costs

    def _validation(self, fare: int, members: list[str]):
        total = 0
        for member_id, cost in self.member_costs:
            total += cost
            if member_id not in members:
                raise domain.VerifyFail(msg='참여 유저가 일치하지 않습니다')

        if total != fare:
            raise domain.VerifyFail(msg='비용이 일치하지 않습니다')

    def create_bills(self, group_id: str, fare: int, members: list[str]) -> list[Bill]:
        self._validation(fare, members)
        bill = Bill(
            id=create_id(),
            group_id=group_id,
            fee=fare,
            charges=[
                Charge(
                    id=create_id(),
                    user_id=member_id,
                    cost=cost
                ) for member_id, cost in self.member_costs
            ]
        )
        return bill
