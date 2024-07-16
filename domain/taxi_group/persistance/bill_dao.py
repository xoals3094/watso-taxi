from typing import List
from pymysql import connect
from domain.taxi_group.entity.bill import Bills, Bill


class MySQLBillDao:
    def __init__(self, connection: connect):
        self.connection = connection

    def find_bills_by_group_id(self, group_id: int) -> Bills:
        sql = f'''
        SELECT user_id, cost 
        FROM bill_table 
        WHERE group_id = {group_id}'''

        cursor = self.connection.cursor()
        cursor.execute(sql)
        datas = cursor.fetchall()

        bills = [Bill(data[0], data[1]) for data in datas]
        cursor.close()

        return Bills(bills)

    def update_bills(self, group_id: int, bills: Bills):
        cursor = self.connection.cursor()

        query = '''
        UPDATE bill_table 
        SET cost = %s
        WHERE group_id = %s AND user_id = %s'''

        data = [(bill.cost, group_id, bill.user_id) for bill in bills.bills]

        cursor.executemany(query, data)
        self.connection.commit()

    def insert_bill(self, group_id: int, user_id: int):
        cursor = self.connection.cursor()

        query = '''
        INSERT INTO bill_table 
        (group_id, user_id, cost)
        VALUES(%s, %s, %s)'''

        data = (group_id, user_id, 0)

        cursor.execute(query, data)
        self.connection.commit()

    def delete_bill(self, group_id: int, user_id: int):
        cursor = self.connection.cursor()

        query = '''
        DELETE FROM bill_table 
        WHERE group_id = %s AND user_id = %s'''

        data = (group_id, user_id)

        cursor.execute(query, data)
        self.connection.commit()
