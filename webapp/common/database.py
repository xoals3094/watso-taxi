from pymysqlpool import ConnectionPool
from config import mysql

pool = ConnectionPool(size=3,
                      host=mysql.host,
                      user=mysql.user,
                      password=mysql.password,
                      port=mysql.port,
                      database=mysql.database)


def get_connection():
    connection = pool.get_connection(pre_ping=True)
    try:
        yield connection
    finally:
        connection.close()


class MySqlDatabase:
    def __init__(self, mysql_connection):
        self.mysql_connection = mysql_connection

    # def _after_method(self, func):
    #     def wrapper(*args, **kwargs):
    #         self.mysql_connection = pool.get_connection(pre_ping=True)
    #         result = func(*args, **kwargs)
    #         self.mysql_connection.close()
    #         return result
    #
    #     return wrapper
    #
    # def __getattribute__(self, item):
    #     attr = super().__getattribute__(item)
    #     if callable(attr):
    #         return super().__getattribute__('_after_method')(attr)
    #     return super().__getattribute__(item)
