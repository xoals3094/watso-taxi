from exceptions import PersistenceException
from pymysql import connect
from domain.group.entity.group import Group
from domain.group.application.group_repository import GroupRepository


class MySQLGroupRepository(GroupRepository):
    def __init__(self, mysql_connection: connect):
        self.connection = mysql_connection

    def find_group_by_id(self, group_id: int) -> Group:
        group_sql = f'''
        SELECT id, owner_id, is_open, max_member 
        FROM group_table
        WHERE id = {group_id}
        '''

        cursor = self.connection.cursor()

        cursor.execute(group_sql)
        group_data = cursor.fetchone()
        if group_data is None:
            raise PersistenceException.ResourceNotFoundException(
                msg=f'그룹 정보를 찾을 수 없습니다. id={group_id}'
            )

        member_sql = f'''
        SELECT group_id, user_id
        FROM group_member_table
        WHERE group_id = {group_id}
        '''
        cursor.execute(member_sql)
        member_data = cursor.fetchall()

        json = {
            'id': group_data[0],
            'owner_id': group_data[1],
            'is_open': group_data[2],
            'member': {
                'max_member': group_data[3],
                'members': [data[1] for data in member_data]
            }
        }

        cursor.close()
        return Group.mapping(json)

    def save(self, group: Group):
        group_sql = f'''
        INSERT INTO group_table
        (id, owner_id, is_open, max_member)
        VALUE({group.id}, {group.owner_id}, {group.is_open}, {group.member.max_member})
        '''

        group_member_sql = f'''
        INSERT INTO group_member_table
        (group_id, user_id)
        VALUE({group.id}, {group.member.members[0]}) 
        '''

        cursor = self.connection.cursor()

        cursor.execute(group_sql)
        cursor.execute(group_member_sql)

        self.connection.commit()
        cursor.close()

    def update_is_open(self, group_id: int, is_open: bool):
        sql = f'''
        UPDATE group_table 
        SET is_open = {is_open} 
        WHERE id = {group_id}'''

        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()

        cursor.close()

    def append_member(self, group_id: int, user_id: int):
        sql = f'''
        INSERT INTO group_member_table 
        (group_id, user_id) VALUE({group_id}, {user_id})'''

        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()

        cursor.close()

    def delete_member(self, group_id: int, user_id: int):
        sql = f'''
        DELETE FROM group_member_table 
        WHERE group_id = {group_id} and user_id = {user_id}'''

        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()

        cursor.close()

    def delete(self, group_id):
        pass
