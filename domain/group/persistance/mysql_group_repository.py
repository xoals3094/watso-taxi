from exceptions import PersistenceException
from pymysql import connect
from bson import ObjectId
from domain.group.entity.group import Group
from domain.group.application.group_repository import GroupRepository


class MySQLGroupRepository(GroupRepository):
    def __init__(self, mysql_connection: connect):
        self.cursor = mysql_connection.cursor()

    def find_group_by_id(self, group_id: str) -> Group:
        sql = f'''
        SELECT id, owner_id, is_open, max_member 
        FROM group_table
        WHERE id = {group_id}
        '''

        self.cursor.execute(sql)
        data = self.cursor.fetchone()
        if data is None:
            raise PersistenceException.ResourceNotFoundException(
                msg=f'그룹 정보를 찾을 수 없습니다. id={group_id}'
            )

        id, owner_id, is_open, max_member = data

        return Group(id, owner_id, is_open, max_member)

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

        self.cursor.execute(group_sql)
        self.cursor.execute(group_member_sql)

    def delete(self, group_id: str):
        find = {'_id': ObjectId(group_id)}
        update = {'$set': {'status': 'canceled'}}
        self.db.group.update_one(find, update)
