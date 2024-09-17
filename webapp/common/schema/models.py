from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, BigInteger, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship


Base = declarative_base()


class UserModel(Base):
    __tablename__ = 'users'

    id = Column(String(32), primary_key=True)
    nickname = Column(String(20), nullable=False)
    profile_image_url = Column(String(200), nullable=False)
    created_at = Column(DateTime, nullable=False)


class KakaoModel(UserModel):
    __tablename__ = 'kakao'

    id = Column(String(32), ForeignKey('users.id'), primary_key=True)
    kakao_id = Column(BigInteger, primary_key=True)


class TokenModel(Base):
    __tablename__ = 'tokens'

    id = Column(String(32), primary_key=True)
    user_id = Column(String(32), ForeignKey('users.id'), nullable=False)
    access_token = Column(String(200), nullable=False)
    refresh_token = Column(String(200), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
