from sqlalchemy import Column, Integer, BigInteger, String, Boolean, DateTime, ForeignKey
from webapp.common.database import Base
from webapp.common.util.id_generator import create_id
from webapp.common.util.token_generator import create_access_token, create_refresh_token
from datetime import datetime


class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True)
    nickname = Column(String, nullable=False)
    profile_image_url = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)

    @staticmethod
    def create(nickname: str, profile_image_url: str):
        return User(
            id=create_id(),
            nickname=nickname,
            profile_image_url=profile_image_url,
            created_at=datetime.now()
        )


class Kakao(Base):
    __tablename__ = 'kakao'

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, nullable=False)

    @staticmethod
    def create(kakao_id: int, user_id: int):
        return Kakao(
            id=kakao_id,
            user_id=user_id,
        )


class Token(Base):
    __tablename__ = 'tokens'

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, nullable=False)
    access_token = Column(String, nullable=False)
    refresh_token = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    @staticmethod
    def create(user_id: int):
        id = create_id()
        return Token(
            id=id,
            user_id=user_id,
            access_token=create_access_token(user_id),
            refresh_token=create_refresh_token(id),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )


class Group(Base):
    __tablename__ = 'groups'

    id = Column(BigInteger, primary_key=True)
    created_at = Column(DateTime, nullable=False)
    owner_id = Column(BigInteger, nullable=False)
    is_open = Column(Boolean, nullable=False)
    max_members = Column(Integer, nullable=False)


class TaxiGroup(Base):
    __tablename__ = 'taxi_groups'

    id = Column(BigInteger, primary_key=True)
    group_id = Column(BigInteger, ForeignKey('groups.id'))
    fare = Column(Integer, nullable=False)
    status = Column(String, nullable=False)
    departure_datetime = Column(DateTime, nullable=False)
    direction = Column(String, nullable=False)


class TaxiGroupMember(Base):
    __tablename__ = 'taxi_group_members'

    id = Column(BigInteger, primary_key=True)
    group_id = Column(BigInteger, ForeignKey('groups.id'))
    user_id = Column(BigInteger, ForeignKey('users.id'))
    cost = Column(Integer, nullable=False)
