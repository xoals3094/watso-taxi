from dependency_injector import containers, providers
from pymysql import connect
from config import mysql
from domain.user.persistance.user_dao import MySQLUserDao
from domain.user.application.user_service import UserService


class UserContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=['app.api.user.user',
                                                            'app.api.taxi_group.chatting'])
    mysql_connection = providers.Singleton(
        connect,
        host=mysql.host,
        user=mysql.user,
        password=mysql.password,
        port=mysql.port,
        database=mysql.database
    )

    user_dao = providers.Singleton(MySQLUserDao, mysql_connection=mysql_connection)
    user_service = providers.Singleton(UserService, user_dao=user_dao)
