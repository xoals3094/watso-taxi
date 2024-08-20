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

    def find_groups(self, user_id, option, direction, depart_datetime) -> List[ResponseGroupSummary]:
        sql = f'''
                    SELECT g.id, owner_id, direction, depart_datetime, status, fee, max_member, 
                    (SELECT COUNT(group_id) FROM group_member_table WHERE group_id = g.id) AS current_member
                    FROM group_table g
                    INNER JOIN taxi_group_table t ON g.id = t.group_id
                    WHERE status = "COMPLETE" 
                    AND depart_datetime >= "{datetime.now() - timedelta(days=90)}"
                    AND g.id NOT IN (SELECT group_id FROM group_member_table WHERE user_id = {user_id}) 
                '''

        if option == 'JOINABLE':
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

        elif option == 'JOINED':
            sql = f'''
                        SELECT g.id, owner_id, direction, depart_datetime, status, fee, max_member, 
                        (SELECT COUNT(group_id) FROM group_member_table WHERE group_id = g.id) AS current_member
                        FROM group_table g
                        INNER JOIN taxi_group_table t ON g.id = t.group_id
                        WHERE status != "COMPLETE"
                        AND g.id IN (SELECT group_id FROM group_member_table WHERE user_id = {user_id}) 
                    '''

        cursor = self.connection.cursor()
        cursor.execute(sql)
        datas = cursor.fetchall()
        datas_json = [
            {
                'id': data[0],
                'owner_id': data[1],
                'direction': data[2],
                'depart_datetime': data[3],
                'status': data[4],
                'fee': data[5],
                'member': {
                    'max_member': data[6],
                    'current_member': data[7]
                }
            }
            for data in datas
        ]
        return [ResponseGroupSummary.mapping(json) for json in datas_json]

    def find_group(self, group_id) -> ResponseGroupDetail:
        group_sql = f'''
        SELECT g.id, owner_id, direction, depart_datetime, status, fee, max_member
        FROM group_table g
        INNER JOIN taxi_group_table t ON g.id = t.group_id
        WHERE g.id = {group_id}
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
        members = [data[0] for data in members_data]

        taxi_group_json = {
            'id': group_data[0],
            'owner_id': group_data[1],
            'direction': group_data[2],
            'depart_datetime': group_data[3],
            'status': Status(group_data[4]),
            'fee': group_data[5],
            'member': {
                'current_member': len(members),
                'max_member': group_data[6],
                'members': members
            }
        }

        cursor.close()
        return ResponseGroupDetail.mapping(taxi_group_json)

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

        json = {
            'fee': fee_data[0],
            'bills': [
                {
                    'user': {
                        'id': bill_data[0],
                        'nickname': bill_data[1]
                    },
                    'cost': bill_data[2]
                } for bill_data in bill_datas]
        }

        return ResponseBills.mapping(json)
