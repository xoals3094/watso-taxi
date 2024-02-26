from abc import *
from typing import List
from logic.taxi.point.dto.PointDto import PointDto


class PointQueryDao(metaclass=ABCMeta):
    @abstractmethod
    def find_points(self) -> List[PointDto]:
        pass
