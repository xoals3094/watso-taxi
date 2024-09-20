from config import mysql

from sqlalchemy import create_engine

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{mysql.user}:{mysql.password}@{mysql.host}/{mysql.database}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)


class MySqlDatabase:
    def __init__(self, session):
        self.session = session
