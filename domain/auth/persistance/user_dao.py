from pymysql import connect
from util.id_generator import create_id


class MySQLUserDao:
    def __init__(self, mysql_connection: connect):
        self.connection = mysql_connection

    def find_id_by_kakao_id(self, kakao_id) -> int | None:
        sql = f'''
        SELECT user_id
        FROM kakao_oauth_table
        WHERE kakao_id = {kakao_id}'''

        cursor = self.connection.cursor()
        cursor.execute(sql)
        data = cursor.fetchone()
        if data is None:
            return None
        return data[0]

    def create(self, kakao_id, nickname, profile_image_url) -> int:
        cursor = self.connection.cursor()

        user_id = create_id()
        user_sql = f'''
        INSERT INTO user_table
        (id, nickname)
        VALUE({user_id}, "{nickname}")'''
        cursor.execute(user_sql)

        kakao_sql = f'''
        INSERT INTO kakao_oauth_table
        (kakao_id, user_id, nickname, profile_image_url)
        VALUE({kakao_id}, {user_id}, "{nickname}", "{profile_image_url}")'''

        cursor.execute(kakao_sql)

        return user_id
