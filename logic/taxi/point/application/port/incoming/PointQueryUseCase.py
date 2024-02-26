from abc import *
from typing import List
from logic.taxi.point.dto.PointDto import PointDto


class PointQueryUseCase(metaclass=ABCMeta):
    @abstractmethod
    def get_list(self) -> List[PointDto]:
        pass
