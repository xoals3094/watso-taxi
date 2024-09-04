from pymysql import connect


class MySqlDatabase:
    def __init__(self, mysql_connection):
        self.mysql_connection: connect = mysql_connection

    def __getattribute__(self, item):
        mysql_connection = super().__getattribute__('mysql_connection')
        mysql_connection.ping(reconnect=True)
        return super().__getattribute__(item)
