from abc import *
from webapp.common.exceptions import domain
from webapp.domain.taxi_group.entity.bill import Bill


class BillingPolicy(metaclass=ABCMeta):
    @abstractmethod
    def create_bills(self, fare: int, members: list[str]) -> list[Bill]:
        pass


class AutoBillingPolicy(BillingPolicy):
    def create_bills(self, fare: int, members: list[str]) -> list[Bill]:
        cost = int(fare / len(members))
        if fare % len(members) == 0:
            cost = int(fare / len(members))
            return [Bill(member_id, cost) for member_id in members]

        rest_cost = fare % len(members)
        owner_cost = cost - (len(members) - rest_cost - 1)
        cost = cost + 1

        owner_id = members[0]
        bills = [Bill(owner_id, owner_cost)]
        for member_id in members[1:]:
            bills.append(Bill(member_id, cost))

        return bills


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

    def create_bills(self, fare: int, members: list[str]) -> list[Bill]:
        self._validation(fare, members)
        bills = [Bill(member_id, cost) for member_id, cost in self.member_costs]
        return bills
