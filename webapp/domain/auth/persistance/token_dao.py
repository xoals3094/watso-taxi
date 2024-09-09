from webapp.common.database import MySqlDatabase
from webapp.domain.auth.exception import persistence


class MySQLTokenDao(MySqlDatabase):
    def find_user_id_by_refresh_token(self, refresh_token) -> int:
        sql = f'''
        SELECT user_id
        FROM token_table
        WHERE refresh_token = "{refresh_token}"'''

        cursor = self.mysql_connection.cursor()
        cursor.execute(sql)
        data = cursor.fetchone()
        if data is None:
            raise persistence.ResourceNotFound

        user_id = data[0]

        return user_id

    def insert(self, user_id, access_token, refresh_token):
        sql = f'''
        INSERT INTO token_table
        (user_id, access_token, refresh_token)
        VALUE({user_id}, "{access_token}", "{refresh_token}")'''

        cursor = self.mysql_connection.cursor()
        cursor.execute(sql)

        self.mysql_connection.commit()

    def delete(self, refresh_token):
        sql = f'DELETE FROM token_table WHERE refresh_token = %s'
        cursor = self.mysql_connection.cursor()
        cursor.execute(sql, refresh_token)
        self.mysql_connection.commit()

    def update_access_token(self, user_id, access_token):
        sql = f'''
        UPDATE token_table 
        SET access_token = "{access_token}" 
        WHERE user_id = {user_id}'''

        cursor = self.mysql_connection.cursor()
        cursor.execute(sql)

        self.mysql_connection.commit()

    def update_both(self, user_id, access_token, refresh_token):
        sql = f'''
        UPDATE token_table 
        SET access_token = "{access_token}",
        refresh_token = "{refresh_token}" 
        WHERE user_id = {user_id}'''

        cursor = self.mysql_connection.cursor()
        cursor.execute(sql)

        self.mysql_connection.commit()
