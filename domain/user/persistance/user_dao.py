from pymysql import connect
from domain.user.dto.response_user import ResponseUser


class MySQLUserDao:
    def __init__(self, mysql_connection: connect):
        self.connection = mysql_connection

    def find_user_by_id(self, user_id) -> ResponseUser:
        sql = 'SELECT id, nickname, profile_image_url FROM user_table WHERE id = %s'
        cursor = self.connection.cursor()
        cursor.execute(sql, user_id)
        data = cursor.fetchone()
        if data is None:
            raise Exception

        user_id, nickname, profile_image_url = data
        return ResponseUser(user_id, nickname, profile_image_url)
