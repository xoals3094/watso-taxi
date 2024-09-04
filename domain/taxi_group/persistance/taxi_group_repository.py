from domain.database import MySqlDatabase
from domain.taxi_group.entity.taxi_group import TaxiGroup
from domain.taxi_group.entity.status import Status
from exceptions import query


class MySQLTaxiGroupRepository(MySqlDatabase):
    def find_taxi_group_by_id(self, group_id) -> TaxiGroup:
        cursor = self.mysql_connection.cursor()
        sql = f'''
        SELECT group_id, fee, status, depart_datetime, direction
        FROM taxi_group_table
        WHERE group_id = {group_id}'''

        cursor.execute(sql)
        data = cursor.fetchone()

        if data is None:
            raise query.ResourceNotFound(
                msg=f'그룹 정보를 찾을 수 없습니다. id={group_id}'
            )

        json = {
            'group_id': data[0],
            'fee': data[1],
            'status': Status(data[2]),
            'depart_datetime': data[3],
            'direction': data[4]
        }

        cursor.close()
        return TaxiGroup.mapping(json)

    def save(self, taxi_group: TaxiGroup):
        cursor = self.mysql_connection.cursor()

        sql = f'''
        INSERT INTO taxi_group_table
        (group_id, fee, status, depart_datetime, direction)
        VALUE({taxi_group.group_id}, {taxi_group.fee}, "{taxi_group.status}", "{taxi_group.depart_datetime}", "{taxi_group.direction}")
        '''
        cursor.execute(sql)
        self.mysql_connection.commit()
        cursor.close()

    def update_status(self, group_id: int, status: Status):
        cursor = self.mysql_connection.cursor()
        sql = f'''
        UPDATE taxi_group_table
        SET status = "{status}"
        WHERE group_id = {group_id}'''

        cursor.execute(sql)
        self.mysql_connection.commit()
        cursor.close()

    def update_fee(self, group_id: int, fee: int):
        cursor = self.mysql_connection.cursor()
        sql = f'''
        UPDATE taxi_group_table
        SET fee = {fee}
        WHERE group_id = {group_id}'''

        cursor.execute(sql)
        self.mysql_connection.commit()
        cursor.close()
