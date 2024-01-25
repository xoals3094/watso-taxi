from datetime import datetime

from logic.taxi.post.application.port.incoming.PostWriteUseCase import PostWriteUseCase
from logic.taxi.post.application.port.outgoing.PostRepository import PostRepository
from logic.taxi.post.application.port.outgoing.PostUpdateDao import PostUpdateDao

from logic.taxi.post.domain.Post import Post

import exceptions


class PostWriteService(PostWriteUseCase):
    def __init__(self, post_repository: PostRepository, post_update_dao: PostUpdateDao):
        self.post_repository = post_repository
        self.post_update_dao = post_update_dao

    def create(self,
               owner_id: str,
               depart_point_id: str,
               arrive_point_id: str,
               depart_datetime: datetime,
               max_member: int,
               notice: str) -> str:
        post = Post.create(owner_id=owner_id,
                           depart_point_id=depart_point_id,
                           arrive_point_id=arrive_point_id,
                           depart_datetime=depart_datetime,
                           max_member=max_member,
                           notice=notice)
        self.post_repository.save(post)
        return post.id

    def delete(self, post_id, user_id):
        try:
            post = self.post_repository.find_post_by_id(post_id)
        except exceptions.NotExistPost:
            raise exceptions.NotExistPost

        post.can_delete(user_id)
        self.post_repository.delete(post.id)

    def modify(self, user_id, post_id, notice):
        try:
            post = self.post_repository.find_post_by_id(post_id)
        except exceptions.NotExistResource:
            raise exceptions.NotExistPost

        post.modify(notice=notice)

        self.post_update_dao.update(post)

    def change_status(self, user_id, post_id, status):
        try:
            post = self.post_repository.find_post_by_id(post_id)
        except exceptions.NotExistResource:
            raise exceptions.NotExistPost

        post.change_status(status)
        self.post_update_dao.update_status(post)

    def join(self, user_id, post_id):
        try:
            post = self.post_repository.find_post_by_id(post_id)
        except exceptions.NotExistResource:
            raise exceptions.NotExistPost

        post.join(user_id)
        self.post_update_dao.update_members(post)

    def quit(self, user_id, post_id):
        try:
            post = self.post_repository.find_post_by_id(post_id)
        except exceptions.NotExistResource:
            raise exceptions.NotExistPost

        post.quit(user_id)
        self.post_update_dao.update_members(post)

