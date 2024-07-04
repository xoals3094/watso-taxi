from typing import List, Tuple


class Charge:
    def __init__(self, user_id: int, cost: int):
        self.user_id = user_id
        self.cost = cost


class Bill:
    def __init__(self, charges: List[Charge]):
        self.charges = charges

    def get_members(self) -> List[int]:
        return [charge.user_id for charge in self.charges]

    def get_total_cost(self) -> int:
        total_cost = 0
        for charge in self.charges:
            total_cost += charge.cost

        return total_cost

    @staticmethod
    def mapping(datas: List[Tuple[int, int]]):
        charges = [Charge(data[0], data[1]) for data in datas]
        return Bill(charges)
