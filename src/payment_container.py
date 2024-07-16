from dependency_injector import containers, providers
from pymysql import connect
from config import mysql

from domain.payment.persistence.kakao_pay_dao import MySQLKakaoPayDao
from domain.payment.persistence.bill_dao import MySQLBillDao
from domain.payment.application.payment_service import PaymentService


class PaymentContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=['app.api.taxi_group.query'])

    connection = providers.Singleton(
        connect,
        host=mysql.host,
        user=mysql.user,
        password=mysql.password,
        port=mysql.port,
        database=mysql.database
    )

    kakao_pay_dao = providers.Singleton(MySQLKakaoPayDao, connection=connection)
    bill_dao = providers.Singleton(MySQLBillDao, connection=connection)

    payment_service = providers.Singleton(PaymentService, kakao_pay_dao=kakao_pay_dao, bill_dao=bill_dao)
