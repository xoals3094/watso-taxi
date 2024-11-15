from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey
)
from sqlalchemy.orm import relationship
from webapp.common.schema.models import Base


class Charge(Base):
    __tablename__ = 'charges'

    id = Column(String(32), primary_key=True)
    bill_id = Column(String(32), ForeignKey('bills.id'))
    user_id = Column(String(32), ForeignKey('users.id'))
    cost = Column(Integer, nullable=False)

    bill = relationship('Bill', back_populates='charges')


class Bill(Base):
    __tablename__ = 'bills'

    id = Column(String(32), primary_key=True)
    group_id = Column(String(32), ForeignKey('groups.id'))
    fee = Column(Integer)

    charges = relationship('Charge', back_populates='bill')
