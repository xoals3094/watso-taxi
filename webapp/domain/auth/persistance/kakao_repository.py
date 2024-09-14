import sqlalchemy.exc
from webapp.common.database import MySqlDatabase
from webapp.common.exceptions import persistence
from webapp.domain.auth.entity.kakao import Kakao


class KakaoRepository(MySqlDatabase):
    def find_by_id(self, kakao_id) -> Kakao:
        try:
            kakao = self.session.query(Kakao).filter(Kakao.kakao_id == kakao_id).one()
        except sqlalchemy.exc.NoResultFound:
            raise persistence.ResourceNotFound

        return kakao

    def save(self, kakao: Kakao):
        self.session.add(kakao)
        self.session.commit()
