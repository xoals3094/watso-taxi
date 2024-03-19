from typing import List

from domain.taxi.point.dto.response_point import ResponsePoint


class MongoDBPointQueryDao:
    def __init__(self, mongodb_connection):
        self.db = mongodb_connection['watso']

    def find_points(self) -> List[ResponsePoint]:
        points_json = self.db.point.find()
        return [ResponsePoint.mapping(point_json) for point_json in points_json]
