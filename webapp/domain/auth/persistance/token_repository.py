import sqlalchemy.exc
from sqlalchemy import delete, select
from webapp.common.database import MySqlDatabase
from webapp.common.exceptions import persistence
from webapp.domain.auth.entity.token import Token


class TokenRepository(MySqlDatabase):
    def find_by_id(self, token_id) -> Token:
        stmt = select(Token).filter_by(id=token_id)
        try:
            token = self.session.execute(stmt).scalar_one()
        except sqlalchemy.exc.NoResultFound:
            raise persistence.ResourceNotFound

        return token

    def save(self, token: Token):
        self.session.add(token)

    def delete(self, token_id: str):
        stmt = delete(Token).filter_by(id=token_id)
        self.session.execute(stmt)
