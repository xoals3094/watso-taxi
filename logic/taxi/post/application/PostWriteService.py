from logic.taxi.post.application.port.incoming.PostWriteUseCase import PostWriteUseCase
from logic.taxi.post.application.port.outgoing.PostRepository import PostRepository
from logic.taxi.post.application.port.outgoing.PostUpdateDao import PostUpdateDao

from logic.taxi.post.domain.Post import Post
from logic.taxi.post.dto.presentation import PostWriteModel

import exceptions


class PostWriteService(PostWriteUseCase):
    def __init__(self, post_repository: PostRepository, post_update_dao: PostUpdateDao):
        self.post_repository = post_repository
        self.post_update_dao = post_update_dao

    def create(self, user_id, post_write_model: PostWriteModel) -> str:
        post = Post.create(user_id=user_id,
                           direction=post_write_model.direction,
                           depart_time=post_write_model.depart_time,
                           max_member=post_write_model.max_member,
                           content=post_write_model.content)
        self.post_repository.save(post)
        return post.id

    def delete(self, post_id, user_id):
        try:
            post = self.post_repository.find_post_by_id(post_id)
        except exceptions.NotExistPost:
            raise exceptions.NotExistPost

        post.can_delete(user_id)
        self.post_repository.delete(post.id)

    def modify(self, user_id, post_id, patch_dict):
        try:
            post = self.post_repository.find_post_by_id(post_id)
        except exceptions.NotExistResource:
            raise exceptions.NotExistPost

        post.modify_content(user_id=user_id, patch_dict=patch_dict)

        self.post_update_dao.update_content(post)

    def change_status(self, user_id, post_id, status):
        try:
            post = self.post_repository.find_post_by_id(post_id)
        except exceptions.NotExistResource:
            raise exceptions.NotExistPost

        post.set_status(user_id, status)
        self.post_update_dao.update_status(post)

    def join(self, post_id, user_id, nickname, order_json):
        try:
            post = self.post_repository.find_post_by_id(post_id)
        except exceptions.NotExistResource:
            raise exceptions.NotExistPost

        post.join(user_id, nickname, order_json)
        self.post_update_dao.update_users(post)

    def quit(self, post_id, user_id):
        try:
            post = self.post_repository.find_post_by_id(post_id)
        except exceptions.NotExistResource:
            raise exceptions.NotExistPost

        post.quit(user_id)
        self.post_update_dao.update_users(post)

