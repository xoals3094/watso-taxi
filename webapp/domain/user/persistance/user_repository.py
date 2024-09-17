import sqlalchemy.exc
from sqlalchemy import select
from webapp.common.database import MySqlDatabase
from webapp.common.exceptions import persistence
from webapp.domain.user.entity.user import User


class UserRepository(MySqlDatabase):
    def find_by_id(self, user_id) -> User:
        stmt = select(User).filter_by(id=user_id)
        try:
            user = self.session.execute(stmt).scalar_one()
        except sqlalchemy.exc.NoResultFound:
            raise persistence.ResourceNotFound

        return user

    def save(self, user: User):
        self.session.add(user)
        self.session.commit()
