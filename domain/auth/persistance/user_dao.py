from domain.database import MySqlDatabase
from util.id_generator import create_id
from domain.auth.exception import persistence


class MySQLUserDao(MySqlDatabase):
    def find_id_by_kakao_id(self, kakao_id) -> int:
        sql = f'''
        SELECT user_id
        FROM kakao_oauth_table
        WHERE kakao_id = {kakao_id}'''

        cursor = self.mysql_connection.cursor()
        cursor.execute(sql)
        data = cursor.fetchone()
        if data is None:
            raise persistence.ResourceNotFound

        user_id = data[0]

        return user_id

    def create(self, kakao_id, nickname, profile_image_url) -> int:
        cursor = self.mysql_connection.cursor()

        user_id = create_id()
        user_sql = f'''
        INSERT INTO user_table
        (id, nickname, profile_image_url)
        VALUE({user_id}, "{nickname}", "{profile_image_url}")'''
        cursor.execute(user_sql)

        kakao_sql = f'''
        INSERT INTO kakao_oauth_table
        (kakao_id, user_id, nickname, profile_image_url)
        VALUE({kakao_id}, {user_id}, "{nickname}", "{profile_image_url}")'''

        cursor.execute(kakao_sql)
        self.mysql_connection.commit()
        return user_id
