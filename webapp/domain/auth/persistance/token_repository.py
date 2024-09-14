import sqlalchemy.exc
from webapp.common.database import MySqlDatabase
from webapp.common.exceptions import persistence
from webapp.domain.auth.entity.token import Token


class TokenRepository(MySqlDatabase):
    def find_by_id(self, token_id) -> Token:
        try:
            token = self.session.query(Token).filter(
                Token.id == token_id
            ).one()
        except sqlalchemy.exc.NoResultFound:
            raise persistence.ResourceNotFound

        return token

    def save(self, token: Token):
        self.session.add(token)
        self.session.commit()

    def delete(self, token_id: str):
        pass
