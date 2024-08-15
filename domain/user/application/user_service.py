from domain.user.persistance.user_dao import MySQLUserDao
from domain.user.dto.response_user import ResponseUser


class UserService:
    def __init__(self, user_dao: MySQLUserDao):
        self.user_dao = user_dao

    def get_user(self, user_id) -> ResponseUser:
        user = self.user_dao.find_user_by_id(user_id)
        return user
