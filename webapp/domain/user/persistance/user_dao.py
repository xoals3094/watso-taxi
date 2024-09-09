from webapp.common.database import MySqlDatabase
from webapp.domain.user.dto.response_user import ResponseUser
from webapp.common.exceptions import query


class MySQLUserDao(MySqlDatabase):
    def find_user_by_id(self, user_id) -> ResponseUser:
        sql = 'SELECT id, nickname, profile_image_url FROM user_table WHERE id = %s'
        cursor = self.mysql_connection.cursor()
        cursor.execute(sql, user_id)
        data = cursor.fetchone()
        if data is None:
            raise query.ResourceNotFound(msg=f'유저 정보를 찾을 수 없습니다 {user_id}')

        user_id, nickname, profile_image_url = data
        return ResponseUser(user_id, nickname, profile_image_url)
