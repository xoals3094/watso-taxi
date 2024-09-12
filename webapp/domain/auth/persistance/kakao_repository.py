from webapp.common.schmea.models import Kakao
from webapp.common.database import MySqlDatabase


class KakaoRepository(MySqlDatabase):
    def find_by_id(self, kakao_id) -> Kakao:
        pass

    def save(self, kakao: Kakao):
        pass
