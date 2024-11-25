from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from webapp.common.util.id_generator import create_id
from webapp.common.schema.models import Base


class Device(Base):
    __tablename__ = 'devices'

    id = Column(String(32), primary_key=True)
    user_id = Column(String(32), ForeignKey('users.id'))
    fcm_token = Column(String(200), nullable=True)
    allow_notification = Column(Boolean, nullable=False)

    user = relationship('User', back_populates='device', uselist=False)

    @staticmethod
    def create(user_id: str, fcm_token: str):
        return Device(
            id=create_id(),
            user_id=user_id,
            fcm_token=fcm_token,
            allow_notification=True
        )
