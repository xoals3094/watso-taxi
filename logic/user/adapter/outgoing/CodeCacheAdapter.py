from logic.user.application.port.outgoing.CodeCacher import CodeCacher
from redis import StrictRedis


class RedisCodeCacher(CodeCacher):
    def __init__(self, redis_connection: StrictRedis):
        self.db = redis_connection

    def get_code_by_email(self, email) -> str:
        return self.db.get(email)

    def save(self, email, code):
        self.db.setex(email, 300, code)

    def delete(self, email):
        self.db.delete(email)
