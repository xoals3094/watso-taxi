from datetime import datetime, timedelta
from sqlalchemy import Column, String, ForeignKey, DateTime
from webapp.common.schema.models import Base
from webapp.common.util.token_generator import create_access_token, create_refresh_token
from webapp.common.util.id_generator import create_id


class Token(Base):
    __tablename__ = 'tokens'

    id = Column(String(32), primary_key=True)
    user_id = Column(String(32), ForeignKey('users.id'), nullable=False)
    access_token = Column(String(200), nullable=False)
    refresh_token = Column(String(200), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    def refresh(self, exp: datetime):
        self.access_token = create_access_token(self.user_id)
        if exp - datetime.now() < timedelta(days=30):
            self.refresh_token = create_refresh_token(self.id)

        self.updated_at = datetime.now()

    @staticmethod
    def create(user_id: str):
        token_id = create_id()
        current_datetime = datetime.now()

        return Token(
            id=token_id,
            user_id=user_id,
            access_token=create_access_token(user_id),
            refresh_token=create_refresh_token(token_id),
            created_at=current_datetime,
            updated_at=current_datetime
        )
