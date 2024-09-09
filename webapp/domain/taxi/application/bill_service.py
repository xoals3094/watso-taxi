from webapp.domain.taxi.persistance.bill_dao import MySQLBillDao
from webapp.domain.taxi.persistance.group_dao import MySQLGroupDao
from webapp.domain.taxi.entity.bill import Bills, Bill


class BillService:

    def __init__(
            self,
            group_dao: MySQLGroupDao,
            bill_dao: MySQLBillDao
    ):
        self.group_dao = group_dao
        self.bill_dao = bill_dao

    def create_bill(
            self,
            group_id,
            user_id
    ):
        self.bill_dao.insert_bill(group_id, user_id)
        self.adjust_bill(group_id)

    def remove_bill(
            self,
            group_id,
            user_id
    ):
        self.bill_dao.delete_bill(group_id, user_id)
        self.adjust_bill(group_id)

    def adjust_bill(
            self,
            group_id
    ):
        owner_id = self.group_dao.find_owner_id_by_group_id(group_id)
        fee = self.group_dao.find_fee_by_group_id(group_id)
        members = self.group_dao.find_members_by_group_id(group_id)

        bills = Bills.adjust(owner_id, fee, members)
        self.bill_dao.update_bills(group_id, bills)

    def set_bill(
            self,
            group_id,
            bills: list[Bill]
    ):
        members = self.group_dao.find_members_by_group_id(group_id)
        fee = self.group_dao.find_fee_by_group_id(group_id)
        Bills.verify(bills, fee, members)

        self.bill_dao.update_bills(group_id, bills)
