from webapp.common.database import MySqlDatabase
from webapp.common.exceptions.persistence import ResourceNotFound


class MySQLGroupDao(MySqlDatabase):
    def find_fee_by_group_id(self, group_id):
        sql = 'SELECT fee FROM taxi_group_table WHERE group_id = %s'
        cursor = self.mysql_connection.cursor()
        cursor.execute(sql, group_id)
        data = cursor.fetchone()
        if data is None:
            raise ResourceNotFound

        return data[0]

    def find_owner_id_by_group_id(self, group_id):
        sql = 'SELECT owner_id FROM group_table WHERE id = %s'
        cursor = self.mysql_connection.cursor()
        cursor.execute(sql, group_id)
        data = cursor.fetchone()
        if data is None:
            raise ResourceNotFound

        return data[0]

    def find_members_by_group_id(self, group_id):
        sql = 'SELECT user_id FROM group_member_table WHERE group_id = %s'
        cursor = self.mysql_connection.cursor()
        cursor.execute(sql, group_id)
        data = cursor.fetchall()

        return list(data)
