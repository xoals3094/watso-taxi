from config import mysql

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{mysql.user}:{mysql.password}@{mysql.host}/{mysql.database}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)


def get_session():
    session = sessionmaker(autocommit=False, autoflush=False, bind=engine)()
    try:
        yield session
    finally:
        session.close()


class MySqlDatabase:
    def __init__(self, session):
        self.session = session
