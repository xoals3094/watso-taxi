from abc import *

from logic.taxi.post.domain.Post import Post


class PostRepository(metaclass=ABCMeta):
    @abstractmethod
    def find_post_by_id(self, post_id) -> Post:
        pass

    @abstractmethod
    def save(self, post: Post):
        pass

    @abstractmethod
    def delete(self, post_id):
        pass
