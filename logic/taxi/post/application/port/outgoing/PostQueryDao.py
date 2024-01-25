from abc import *
from typing import List
from logic.taxi.post.dto.PostSummaryDto import PostSummaryDto
from logic.taxi.post.dto.PostDetailDto import PostDetailDto


class PostQueryDao(metaclass=ABCMeta):
    @abstractmethod
    def find_posts(self, user_id, depart_point_id, arrive_point_id, depart_datetime) -> List[PostSummaryDto]:
        pass

    @abstractmethod
    def find_post_by_id(self, post_id) -> PostDetailDto:
        pass
