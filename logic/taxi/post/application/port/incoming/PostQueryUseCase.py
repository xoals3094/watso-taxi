from abc import *
from typing import List
from datetime import datetime
from logic.taxi.post.dto.PostSummaryDto import PostSummaryDto
from logic.taxi.post.dto.PostDetailDto import PostDetailDto


class PostQueryUseCase(metaclass=ABCMeta):
    @abstractmethod
    def get_list(self, user_id, depart_point, arrive_point, depart_datetime: datetime) -> List[PostSummaryDto]:
        pass

    @abstractmethod
    def get(self, post_id) -> PostDetailDto:
        pass
