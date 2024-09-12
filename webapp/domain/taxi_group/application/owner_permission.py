from fastapi import Depends
from webapp.common.util.token_decoder import get_user_id

from webapp.common.exceptions import auth
from webapp.common.database import pool
from webapp.common.exceptions import query


def find_owner_id_by_group_id(group_id) -> int:
    connection = pool.get_connection(pre_ping=True)
    cursor = connection.mysql_connection.cursor()
    sql = f'''
    SELECT owner_id
    FROM group_table
    WHERE id = {group_id}'''

    cursor.execute(sql)
    data = cursor.fetchone()

    if data is None:
        raise query.ResourceNotFound(
            msg=f'그룹 정보를 찾을 수 없습니다. id={group_id}'
        )

    cursor.close()
    owner_id = data[0]
    return owner_id


def owner_permission(
        group_id: int,
        user_id: int = Depends(get_user_id)
):
    owner_id = find_owner_id_by_group_id(group_id)
    if owner_id != user_id:
        raise auth.AccessDenied(msg='그룹 수정 권한이 없습니다')
    return
