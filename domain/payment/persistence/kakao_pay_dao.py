from domain.database import MySqlDatabase


class MySQLKakaoPayDao(MySqlDatabase):
    def find_kakao_pay_user_id_by_user_id(self, user_id) -> str:
        sql = 'SELECT kakao_pay_id FROM kakao_pay_table WHERE user_id = %s'
        cursor = self.mysql_connection.cursor()

        cursor.execute(sql, user_id)

        data = cursor.fetchone()
        kakao_pay_id = data[0]

        return kakao_pay_id
