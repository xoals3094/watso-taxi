from typing import List

from logic.taxi.point.dto.PointDto import PointDto
from logic.taxi.point.application.port.outgoing.PointQueryDao import PointQueryDao


class MongoDBPointQueryDao(PointQueryDao):
    def __init__(self, mongodb_connection):
        self.db = mongodb_connection['watso']

    def find_points(self) -> List[PointDto]:
        points_json = self.db.point.find()
        return [PointDto.mapping(point_json) for point_json in points_json]
