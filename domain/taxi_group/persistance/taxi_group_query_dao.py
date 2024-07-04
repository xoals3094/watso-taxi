from pymysql import connect
from typing import List
from domain.taxi_group.entity.status import Status
from domain.taxi_group.dto.response_group_detail import ResponseGroupDetail
from domain.taxi_group.dto.response_group_summary import ResponseGroupSummary
from exceptions import PersistenceException


class MySQLTaxiGroupQueryDao:
    def __init__(self, mysql_connection: connect):
        self.mysql_connection = mysql_connection

    def find_groups(self, user_id, direction, depart_datetime) -> List[ResponseGroupSummary]:
        sql = f'''
        SELECT g.id, owner_id, u.nickname, direction, depart_datetime, status, fee, max_member, 
        (SELECT COUNT(group_id) FROM group_member_table WHERE group_id = g.id) AS current_member
        FROM group_table g
        INNER JOIN taxi_group_table t ON g.id = t.group_id
        LEFT JOIN user_table u ON owner_id = u.id
        WHERE is_open = true 
        AND direction = "{direction}" 
        AND depart_datetime >= "{depart_datetime}"
        AND g.id NOT IN (SELECT group_id FROM group_member_table WHERE user_id = {user_id}) 
        '''

        cursor = self.mysql_connection.cursor()
        cursor.execute(sql)
        datas = cursor.fetchall()
        datas_json = [
            {
                'id': data[0],
                'owner': {
                    'id': data[1],
                    'nickname': data[2],
                },
                'direction': data[3],
                'depart_datetime': data[4],
                'status': data[5],
                'fee': data[6],
                'member': {
                    'max_member': data[7],
                    'current_member': data[8]
                }
            }
            for data in datas
        ]

        return [ResponseGroupSummary.mapping(json) for json in datas_json]

    def find_group(self, group_id) -> ResponseGroupDetail:
        group_sql = f'''
        SELECT g.id, owner_id, u.nickname, direction, depart_datetime, status, fee, max_member
        FROM group_table g
        INNER JOIN taxi_group_table t ON g.id = t.group_id
        LEFT JOIN user_table u ON owner_id = u.id
        WHERE g.id = {group_id}
        '''

        cursor = self.mysql_connection.cursor()
        cursor.execute(group_sql)
        group_data = cursor.fetchone()
        if group_data is None:
            raise PersistenceException.ResourceNotFoundException(
                msg=f'그룹 정보를 찾을 수 없습니다. id={group_id}'
            )

        member_sql = f'''
        SELECT user_id FROM group_member_table 
        WHERE group_id = {group_id}'''

        cursor.execute(member_sql)
        members_data = cursor.fetchall()
        members = [data[0] for data in members_data]

        taxi_group_json = {
            'id': group_data[0],
            'owner': {
                'id': group_data[1],
                'nickname': group_data[2]
            },
            'direction': group_data[3],
            'depart_datetime': group_data[4],
            'status': Status(group_data[5]),
            'fee': group_data[6],
            'member': {
                'current_member': len(members),
                'max_member': group_data[7],
                'members': members
            }
        }

        cursor.close()
        return ResponseGroupDetail.mapping(taxi_group_json)
