from pymysql import connect
from typing import List
from domain.taxi_group.entity.status import Status
from query.taxi_group.dto.response_group_detail import ResponseGroupDetail
from query.taxi_group.dto.response_group_summary import ResponseGroupSummary
from query.taxi_group.dto.response_bill import ResponseBills
from exceptions import query
from datetime import datetime, timedelta


class MySQLTaxiGroupQueryDao:
    def __init__(self, connection: connect):
        self.connection = connection

    @staticmethod
    def costed_group_list_mapping(data_list):
        datas_json = []
        for data in data_list:
            id, owner_id, direction, depart_datetime, status, fee, max_member, current_member, cost = data
            json = {
                'id': id,
                'owner_id': owner_id,
                'direction': direction,
                'depart_datetime': depart_datetime,
                'status': status,
                'fee': {
                    'total': fee,
                    'cost': cost,
                },
                'member': {
                    'max_member': max_member,
                    'current_member': current_member
                }
            }
            datas_json.append(json)

        return datas_json

    def find_complete_groups(self, user_id) -> List[ResponseGroupSummary]:
        sql = f'''
                    SELECT g.id, owner_id, direction, depart_datetime, status, fee, max_member,
                    (SELECT COUNT(group_id) FROM group_member_table WHERE group_id = g.id) AS current_member, bt.cost 
                    FROM group_table g
                    INNER JOIN taxi_group_table t ON g.id = t.group_id
                    LEFT JOIN bill_table bt ON g.id = bt.group_id
                    WHERE status = "COMPLETE"
                    AND depart_datetime >= "{datetime.now() - timedelta(days=90)}"
                    AND g.id IN (SELECT group_id FROM group_member_table WHERE user_id = {user_id}) 
                    AND bt.user_id = {user_id}
                '''

        cursor = self.connection.cursor()
        cursor.execute(sql)
        datas = cursor.fetchall()
        datas_json = self.costed_group_list_mapping(datas)

        return [ResponseGroupSummary.mapping(json) for json in datas_json]

    @staticmethod
    def group_list_mapping(data_list):
        datas_json = []
        for data in data_list:
            id, owner_id, direction, depart_datetime, status, fee, max_member, current_member = data
            json = {
                'id': id,
                'owner_id': owner_id,
                'direction': direction,
                'depart_datetime': depart_datetime,
                'status': status,
                'fee': {
                    'total': fee,
                    'cost': int(fee / (current_member + 1)),
                },
                'member': {
                    'max_member': max_member,
                    'current_member': current_member
                }
            }
            datas_json.append(json)

        return datas_json

    def find_joinable_groups(self, user_id, direction, depart_datetime):
        sql = f'''
                    SELECT g.id, owner_id, direction, depart_datetime, status, fee, max_member, 
                    (SELECT COUNT(group_id) FROM group_member_table WHERE group_id = g.id) AS current_member
                    FROM group_table g
                    INNER JOIN taxi_group_table t ON g.id = t.group_id
                    WHERE is_open = true 
                    AND direction = "{direction}" 
                    AND depart_datetime >= "{depart_datetime}"
                    AND g.id NOT IN (SELECT group_id FROM group_member_table WHERE user_id = {user_id})
                '''

        cursor = self.connection.cursor()
        cursor.execute(sql)
        datas = cursor.fetchall()
        datas_json = self.group_list_mapping(datas)
        return [ResponseGroupSummary.mapping(json) for json in datas_json]

    def find_joined_groups(self, user_id):
        sql = f'''
                    SELECT g.id, owner_id, direction, depart_datetime, status, fee, max_member, 
                    (SELECT COUNT(group_id) FROM group_member_table WHERE group_id = g.id) AS current_member, bt.cost 
                    FROM group_table g
                    INNER JOIN taxi_group_table t ON g.id = t.group_id
                    LEFT JOIN bill_table bt ON g.id = bt.group_id
                    WHERE status != "COMPLETE"
                    AND g.id IN (SELECT group_id FROM group_member_table WHERE user_id = {user_id}) 
                    AND bt.user_id = {user_id}
                '''

        cursor = self.connection.cursor()
        cursor.execute(sql)
        datas = cursor.fetchall()
        datas_json = self.costed_group_list_mapping(datas)
        return [ResponseGroupSummary.mapping(json) for json in datas_json]

    @staticmethod
    def group_detail_json_mapping(group_data, members_data):
        members = [data[0] for data in members_data]
        id, owner_id, direction, depart_datetime, status, fee, max_member, cost = group_data
        json = {
            'id': id,
            'owner_id': owner_id,
            'direction': direction,
            'depart_datetime': depart_datetime,
            'status': status,
            'fee': {
                'total': fee,
                'cost': cost,
            },
            'member': {
                'current_member': len(members),
                'max_member': max_member,
                'members': members
            }
        }

        return json

    def find_group(self, user_id, group_id) -> ResponseGroupDetail:
        group_sql = f'''
        SELECT g.id, owner_id, direction, depart_datetime, status, fee, max_member, bt.cost 
        FROM group_table g
        INNER JOIN taxi_group_table t ON g.id = t.group_id
        LEFT JOIN bill_table bt ON g.id = bt.group_id
        WHERE g.id = {group_id}
        AND bt.user_id = {user_id}
        '''

        cursor = self.connection.cursor()
        cursor.execute(group_sql)
        group_data = cursor.fetchone()
        if group_data is None:
            raise query.ResourceNotFound(msg='그룹 정보를 찾을 수 없습니다')

        member_sql = f'''
        SELECT user_id FROM group_member_table 
        WHERE group_id = {group_id}'''

        cursor.execute(member_sql)
        members_data = cursor.fetchall()
        taxi_group_json = self.group_detail_json_mapping(group_data, members_data)
        return ResponseGroupDetail.mapping(taxi_group_json)

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

        cursor = self.connection.cursor()
        cursor.execute(bill_sql, group_id)
        bill_datas = cursor.fetchall()

        fee_sql = 'SELECT fee FROM taxi_group_table WHERE group_id = %s'
        cursor.execute(fee_sql, group_id)
        fee_data = cursor.fetchone()

        json = self.bills_json_mapping(fee_data, bill_datas)

        return ResponseBills.mapping(json)
