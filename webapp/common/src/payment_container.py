from webapp.domain.payment.persistence.kakao_pay_dao import MySQLKakaoPayDao
from webapp.domain.payment.persistence.bill_dao import MySQLBillDao
from webapp.domain.payment.application.payment_service import PaymentService


class PaymentContainer:
    kakao_pay_dao = MySQLKakaoPayDao()
    bill_dao = MySQLBillDao()

    payment_service = PaymentService(kakao_pay_dao=kakao_pay_dao, bill_dao=bill_dao)
