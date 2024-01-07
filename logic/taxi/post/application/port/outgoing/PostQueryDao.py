from abc import *
from typing import List
from logic.taxi.post.dto.PostSummaryDto import PostSummaryDto
from logic.taxi.post.dto.PostDetailDto import PostDetailDto


class PostQueryDao(metaclass=ABCMeta):
    @abstractmethod
    def find_joinable_posts_by_user_id(self, user_id) -> List[PostSummaryDto]:
        pass

    @abstractmethod
    def find_joined_posts_by_user_id(self, user_id) -> List[PostSummaryDto]:
        pass

    @abstractmethod
    def find_all_posts_by_user_id(self, user_id) -> List[PostSummaryDto]:
        pass

    @abstractmethod
    def find_post_by_id(self, post_id) -> PostDetailDto:
        pass
