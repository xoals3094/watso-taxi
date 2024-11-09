from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey
)
from webapp.common.schema.models import Base


class Bill(Base):
    __tablename__ = 'taxi_group_bills'

    id = Column(String(32), primary_key=True)
    group_id = Column(String(32), ForeignKey('groups.id'))
    user_id = Column(String(32), ForeignKey('users.id'))
    cost = Column(Integer, nullable=False)
