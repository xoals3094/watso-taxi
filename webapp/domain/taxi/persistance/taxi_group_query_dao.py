from typing import List
from datetime import datetime, timedelta

from webapp.common.exceptions import query
from webapp.common.database import MySqlDatabase


class MySQLTaxiGroupQueryDao(MySqlDatabase):
    def find_complete_groups(self, user_id) -> List[ResponseTaxiGroup]:
        sql = f'''
                    SELECT g.id, owner_id, direction, depart_datetime, status, fee, bt.cost, max_member,
                    (SELECT COUNT(group_id) FROM group_member_table WHERE group_id = g.id) AS current_member
                    FROM group_table g
                    INNER JOIN taxi_group_table t ON g.id = t.group_id
                    LEFT JOIN bill_table bt ON g.id = bt.group_id
                    WHERE status = "COMPLETE"
                    AND depart_datetime >= "{datetime.now() - timedelta(days=90)}"
                    AND g.id IN (SELECT group_id FROM group_member_table WHERE user_id = {user_id}) 
                    AND bt.user_id = {user_id}
                '''

        cursor = self.mysql_connection.cursor()
        cursor.execute(sql)
        datas = cursor.fetchall()
        json_list = [
            {
                'id': data[0],
                'owner_id': data[1],
                'direction': data[2],
                'depart_datetime': data[3],
                'status': data[4],
                'fee': {
                    'total': data[5],
                    'cost': data[6],
                },
                'member': {
                    'max_member': data[7],
                    'current_member': data[8]
                }
            }
            for data in datas
        ]

        return [ResponseTaxiGroup.mapping(json) for json in json_list]

    def find_joinable_groups(self, user_id, direction, departure_datetime):
        sql = f'''
            SELECT g.id, owner_id, direction, departure_datetime, status, fee, max_members, 
            (SELECT COUNT(group_id) FROM group_member_table WHERE group_id = g.id) AS current_member
            FROM group_table g
            INNER JOIN taxi_group_table t ON g.id = t.group_id
            WHERE is_open = true
            AND departure_datetime >= "{departure_datetime}"
            AND g.id NOT IN (SELECT group_id FROM group_member_table WHERE user_id = {user_id})
            AND direction = "{direction}" 
        '''

        cursor = self.mysql_connection.cursor()
        cursor.execute(sql)
        datas = cursor.fetchall()
        json_list = [
            {
                'id': data[0],
                'owner_id': data[1],
                'direction': data[2],
                'depart_datetime': data[3],
                'status': data[4],
                'fee': {
                    'total': data[5],
                    'cost': int(data[5] / data[7] + 1),
                },
                'member': {
                    'max_member': data[6],
                    'current_member': data[7]
                }
            }
            for data in datas
        ]
        return [ResponseTaxiGroup.mapping(json) for json in json_list]

    def find_joined_groups(self, user_id):
        sql = f'''
                    SELECT g.id, owner_id, direction, depart_datetime, status, fee, bt.cost , max_member, 
                    (SELECT COUNT(group_id) FROM group_member_table WHERE group_id = g.id) AS current_member 
                    FROM group_table g
                    INNER JOIN taxi_group_table t ON g.id = t.group_id
                    LEFT JOIN bill_table bt ON g.id = bt.group_id
                    WHERE status != "COMPLETE"
                    AND g.id IN (SELECT group_id FROM group_member_table WHERE user_id = {user_id}) 
                    AND bt.user_id = {user_id}
                '''

        cursor = self.mysql_connection.cursor()
        cursor.execute(sql)
        datas = cursor.fetchall()
        json_list = [
            {
                'id': data[0],
                'owner_id': data[1],
                'direction': data[2],
                'depart_datetime': data[3],
                'status': data[4],
                'fee': {
                    'total': data[5],
                    'cost': data[6],
                },
                'member': {
                    'max_member': data[7],
                    'current_member': data[8]
                }
            }
            for data in datas
        ]
        return [ResponseTaxiGroup.mapping(json) for json in json_list]

    def find_group(self, user_id, group_id) -> ResponseTaxiGroup:
        group_sql = f'''
        SELECT g.id, owner_id, direction, depart_datetime, status, fee, bt.cost, max_member,
        (SELECT COUNT(group_id) FROM group_member_table WHERE group_id = g.id) AS current_member
        FROM group_table g
        INNER JOIN taxi_group_table t ON g.id = t.group_id
        LEFT JOIN bill_table bt ON g.id = bt.group_id
        WHERE g.id = {group_id}
        AND bt.user_id = {user_id}
        '''

        cursor = self.mysql_connection.cursor()
        cursor.execute(group_sql)
        data = cursor.fetchone()
        if data is None:
            raise query.ResourceNotFound(msg='그룹 정보를 찾을 수 없습니다')

        json = {
            'id': data[0],
            'owner_id': data[1],
            'direction': data[2],
            'depart_datetime': data[3],
            'status': data[4],
            'fee': {
                'total': data[5],
                'cost': data[6],
            },
            'member': {
                'max_member': data[7],
                'current_member': data[8]
            }
        }
        return ResponseTaxiGroup.mapping(json)

    @staticmethod
    def bills_json_mapping(fee_data, bills_data):
        json = {
            'fee': fee_data[0],
            'bills': [
                {
                    'user': {
                        'id': bill_data[0],
                        'nickname': bill_data[1]
                    },
                    'cost': bill_data[2]
                } for bill_data in bills_data]
        }

        return json

    def find_bills_by_group_id(self, group_id: int) -> ResponseBills:
        bill_sql = '''
        SELECT u.id as user_id, u.nickname, b.cost 
        FROM bill_table b 
        INNER JOIN user_table u ON b.user_id = u.id
        WHERE group_id = %s'''

        cursor = self.mysql_connection.cursor()
        cursor.execute(bill_sql, group_id)
        bill_datas = cursor.fetchall()

        fee_sql = 'SELECT fee FROM taxi_group_table WHERE group_id = %s'
        cursor.execute(fee_sql, group_id)
        fee_data = cursor.fetchone()

        json = self.bills_json_mapping(fee_data, bill_datas)

        return ResponseBills.mapping(json)
