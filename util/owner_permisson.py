from util.token_decoder import get_user_id
from fastapi import Depends
from exceptions import AuthenticationException
from pymysql import connect
from config.production import mysql

mysql = connect(host=mysql.host,
                user=mysql.user,
                password=mysql.password,
                port=mysql.port,
                database=mysql.database)


def owner_permission(func, user_id=Depends(get_user_id)):
    def wrap(*args, **kwargs):
        cursor = mysql.cursor()
        sql = f'''
        SELECT id FROM group WHERE id={kwargs['group_id']}
        '''
        cursor.execute(sql)
        owner_id = cursor.fetchone()[0]
        if user_id != owner_id:
            raise AuthenticationException.AccessDeniedException
        return func(*args, **kwargs)
    return wrap
