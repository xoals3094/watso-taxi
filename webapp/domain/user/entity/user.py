from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from webapp.common.util.id_generator import create_id
from webapp.common.schema.models import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(String(32), primary_key=True)
    nickname = Column(String(20), nullable=False)
    profile_image_url = Column(String(200), nullable=False)
    created_at = Column(DateTime, nullable=False)

    tokens = relationship('Token', back_populates='user')
    device = relationship('Device', back_populates='user', uselist=False)
    kakao = relationship('Kakao', back_populates='user', uselist=False)

    @staticmethod
    def create(nickname: str, profile_image_url: str):
        return User(
            id=create_id(),
            nickname=nickname,
            profile_image_url=profile_image_url,
            created_at=datetime.now()
        )
