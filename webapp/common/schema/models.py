from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, BigInteger, String, Boolean, DateTime, ForeignKey
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


class GroupModel(Base):
    __tablename__ = 'groups'

    id = Column(String(32), primary_key=True)
    created_at = Column(DateTime, nullable=False)
    owner_id = Column(String(32), nullable=False)
    is_open = Column(Boolean, nullable=False)
    max_members = Column(Integer, nullable=False)

    members = relationship('MemberModel')


class MemberModel(Base):
    __tablename__ = 'members'

    id = Column(String(32), primary_key=True)
    group_id = Column(String(32), ForeignKey('groups.id'))
    user_id = Column(String(32), ForeignKey('users.id'))


class TaxiGroupMemberModel(MemberModel):
    __tablename__ = 'taxi_group_members'

    id = Column(String(32), ForeignKey('members.id'), primary_key=True)
    cost = Column(Integer, nullable=False)


class TaxiGroupModel(GroupModel):
    __tablename__ = 'taxi_groups'

    id = Column(String(32), ForeignKey('groups.id'), primary_key=True)
    fare = Column(Integer, nullable=False)
    status = Column(String(20), nullable=False)
    departure_datetime = Column(DateTime, nullable=False)
    direction = Column(String(20), nullable=False)

    members = relationship('TaxiGroupMemberModel')
