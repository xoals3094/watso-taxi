from sqlalchemy import Column, String, Boolean, ForeignKey
from webapp.common.util.id_generator import create_id
from webapp.common.schema.models import Base


class Device(Base):
    __tablename__ = 'devices'

    id = Column(String(32), primary_key=True)
    user_id = Column(String(32), ForeignKey('users.id'))
    fcm_token = Column(String(32), nullable=True)
    allow_notification = Column(Boolean, nullable=False)

    @staticmethod
    def create(user_id: str, fcm_token: str):
        return Device(
            id=create_id(),
            nickname=user_id,
            profile_image_url=fcm_token,
            allow_notification=True
        )
