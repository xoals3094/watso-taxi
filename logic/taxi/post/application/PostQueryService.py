from typing import List
from logic.taxi.post.application.port.incoming.PostQueryUseCase import PostQueryUseCase
from logic.taxi.post.application.port.outgoing.PostQueryDao import PostQueryDao
from logic.taxi.post.dto.PostSummaryDto import PostSummaryDto
from logic.taxi.post.dto.PostDetailDto import PostDetailDto
import exceptions


class PostQueryService(PostQueryUseCase):
    def __init__(self, post_query_dao: PostQueryDao):
        self.post_query_dao = post_query_dao

    def get_list(self, option, user_id) -> List[PostSummaryDto]:
        if option == 'joinable':
            return self.post_query_dao.find_joinable_posts_by_user_id(user_id)

        elif option == 'joined':
            return self.post_query_dao.find_joined_posts_by_user_id(user_id)

        elif option == 'all':
            return self.post_query_dao.find_all_posts_by_user_id(user_id)

    def get(self, post_id) -> PostDetailDto:
        try:
            post = self.post_query_dao.find_post_by_id(post_id)
        except exceptions.NotExistResource:
            raise exceptions.NotExistPost

        return post
