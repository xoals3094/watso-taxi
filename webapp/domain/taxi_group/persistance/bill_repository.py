from webapp.common.database import MySqlDatabase
from webapp.domain.taxi_group.entity.bill import Bill


class BillRepository(MySqlDatabase):
    def save(self, bills: list[Bill]):
        for bill in bills:
            self.session.add(bill)
