from domain.payment.persistence.kakao_pay_dao import MySQLKakaoPayDao
from domain.payment.persistence.bill_dao import MySQLBillDao
from domain.payment.util import kakao_pay


class PaymentService:
    def __init__(self, kakao_pay_dao: MySQLKakaoPayDao, bill_dao: MySQLBillDao):
        self.kakao_pay_dao = kakao_pay_dao
        self.bill_dao = bill_dao

    def create_url(self, group_id: int, user_id: int) -> str:
        cost = self.bill_dao.find_cost(group_id, user_id)
        kakao_pay_user_id = self.kakao_pay_dao.find_kakao_pay_user_id_by_user_id(user_id)
        url = kakao_pay.create_url(kakao_pay_user_id, cost)

        return url
