from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey
)
from sqlalchemy.orm import relationship
from webapp.common.schema.models import Base
from webapp.common.exceptions import domain


class Member(Base):
    __tablename__ = 'members'

    id = Column(String(32), primary_key=True)
    type = Column(String(20))
    group_id = Column(String(32), ForeignKey('groups.id'))
    user_id = Column(String(32), ForeignKey('users.id'))

    __mapper_args__ = {
        'polymorphic_identity': 'member',
        'polymorphic_on': 'type'
    }


class Group(Base):
    __tablename__ = 'groups'

    id = Column(String(32), primary_key=True)
    type = Column(String(20))
    created_at = Column(DateTime, nullable=False)
    owner_id = Column(String(32), nullable=False)
    is_open = Column(Boolean, nullable=False)
    max_members = Column(Integer, nullable=False)

    members = relationship('Member', cascade='delete, delete-orphan')

    __mapper_args__ = {
        'polymorphic_identity': 'group',
        'polymorphic_on': 'type'
    }

    def open(self):
        self.is_open = True

    def close(self):
        self.is_open = False

    def participate(self, member: Member):
        if self.owner_id == member.user_id:
            raise domain.ParticipationFailed(msg=f'그룹장 유저는 참여가 불가능합니다')

        if self.is_open is False:
            raise domain.ParticipationFailed(msg=f'참여가 마감된 그룹입니다 is_open={self.is_open}')

        if self.max_members <= len(self.members):
            raise domain.ParticipationFailed(msg=f'최대 인원에 도달하여 참여 불가능합니다 {len(self.members)}/{self.max_members}')

        for group_member in self.members:
            if member.user_id == group_member.user_id:
                raise domain.ParticipationFailed(msg='이미 참여한 유저입니다')
        self.members.append(member)

    def leave(self, user_id):
        if self.owner_id == user_id:
            raise domain.ParticipationFailed(msg=f'그룹장 유저는 탈퇴가 불가능합니다')

        if self.is_open is False:
            raise domain.ParticipationFailed(msg=f'탈퇴가 불가능한 그룹입니다 is_open={self.is_open}')

        for group_member in self.members:
            if user_id == group_member.user_id:
                self.members.remove(group_member)
                return
        raise domain.LeaveFailed(msg='참여하지 않은 유저입니다')
