from sqlalchemy import Column, BigInteger, String, ForeignKey
from webapp.common.schema.models import Base


class Kakao(Base):
    __tablename__ = 'kakao'

    id = Column(BigInteger, primary_key=True)
    user_id = Column(String(32), ForeignKey('users.id'))

    @staticmethod
    def create(
            kakao_id: int,
            user_id: str,
    ):

        return Kakao(
            id=kakao_id,
            user_id=user_id
        )
