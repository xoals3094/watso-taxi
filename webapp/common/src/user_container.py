from webapp.domain.user.persistance.user_dao import MySQLUserDao
from webapp.domain.user.application.user_service import UserService


class UserContainer:
    user_dao = MySQLUserDao()
    user_service = UserService(user_dao=user_dao)
