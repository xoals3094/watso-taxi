from abc import *
from typing import List
from logic.taxi.post.dto.PostSummaryDto import PostSummaryDto
from logic.taxi.post.dto.PostDetailDto import PostDetailDto


class PostQueryUseCase(metaclass=ABCMeta):
    @abstractmethod
    def get_list(self, option, user_id) -> List[PostSummaryDto]:
        pass

    @abstractmethod
    def get(self, post_id) -> PostDetailDto:
        pass
