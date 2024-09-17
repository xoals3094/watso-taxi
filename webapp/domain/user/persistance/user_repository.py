import sqlalchemy.exc
from webapp.common.database import MySqlDatabase
from webapp.common.exceptions import persistence
from webapp.domain.user.entity.user import User


class UserRepository(MySqlDatabase):
    def find_by_id(self, user_id) -> User:
        try:
            user = self.session.query(User).filter(
                User.id == user_id
            ).one()
        except sqlalchemy.exc.NoResultFound:
            raise persistence.ResourceNotFound

        return user

    def save(self, user: User):
        self.session.add(user)
        self.session.commit()
