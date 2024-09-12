from webapp.common.database import MySqlDatabase
from webapp.common.exceptions import persistence
from webapp.common.schmea.models import Token


class TokenRepository(MySqlDatabase):
    def find_by_id(self, token_id) -> Token:
        pass

    def save(self, token: Token):
        pass

    def delete(self, token_id: int):
        pass
