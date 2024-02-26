from typing import List
from logic.taxi.post.application.port.incoming.PostQueryUseCase import PostQueryUseCase
from logic.taxi.post.application.port.outgoing.PostQueryDao import PostQueryDao
from logic.taxi.post.dto.PostSummaryDto import PostSummaryDto
from logic.taxi.post.dto.PostDetailDto import PostDetailDto


class PostQueryService(PostQueryUseCase):
    def __init__(self, post_query_dao: PostQueryDao):
        self.post_query_dao = post_query_dao

    def get_list(self, user_id, depart_point_id, arrive_point_id, depart_datetime) -> List[PostSummaryDto]:
        return self.post_query_dao.find_posts(user_id, depart_point_id, arrive_point_id, depart_datetime)

    def get(self, post_id) -> PostDetailDto:
        post = self.post_query_dao.find_post_by_id(post_id)
        return post
