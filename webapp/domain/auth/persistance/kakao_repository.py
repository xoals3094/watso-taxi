import sqlalchemy.exc
from sqlalchemy import select
from webapp.common.database import MySqlDatabase
from webapp.common.exceptions import persistence
from webapp.domain.auth.entity.kakao import Kakao


class KakaoRepository(MySqlDatabase):
    def find_by_id(self, kakao_id) -> Kakao:
        stmp = select(Kakao).filter_by(id=kakao_id)

        try:
            kakao = self.session.execute(stmp).scalar_one()
        except sqlalchemy.exc.NoResultFound:
            raise persistence.ResourceNotFound

        return kakao

    def save(self, kakao: Kakao):
        self.session.add(kakao)
        self.session.commit()
