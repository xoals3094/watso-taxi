from typing import List
from logic.taxi.point.application.port.incoming.PointQueryUseCase import PointQueryUseCase
from logic.taxi.point.application.port.outgoing.PointQueryDao import PointQueryDao
from logic.taxi.point.dto.PointDto import PointDto


class PointQueryService(PointQueryUseCase):
    def __init__(self, point_query_dao: PointQueryDao):
        self.point_query_dao = point_query_dao

    def get_list(self) -> List[PointDto]:
        return self.point_query_dao.find_points()
