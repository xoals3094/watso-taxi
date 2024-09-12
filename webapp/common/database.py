from pymysqlpool import ConnectionPool
from config import mysql

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
SQLALCHEMY_DATABASE_URL = "sqlite:///./myapi.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
pool = ConnectionPool(size=3,
                      host=mysql.host,
                      user=mysql.user,
                      password=mysql.password,
                      port=mysql.port,
                      database=mysql.database)


def get_connection():
    connection = pool.get_connection(pre_ping=True)
    try:
        yield connection
    finally:
        connection.close()


class MySqlDatabase:
    def __init__(self, session: SessionLocal):
        self.session = session
