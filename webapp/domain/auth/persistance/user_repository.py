from webapp.common.database import MySqlDatabase
from webapp.common.schmea.models import User


class UserRepository(MySqlDatabase):
    def find_by_id(self, user_id) -> User:
        pass

    def save(self, user: User):
        pass
