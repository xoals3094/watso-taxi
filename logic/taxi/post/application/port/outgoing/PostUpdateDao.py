from abc import *
from logic.taxi.post.domain.Post import Post


class PostUpdateDao(metaclass=ABCMeta):
    @abstractmethod
    def update(self, post: Post):
        pass

    @abstractmethod
    def update_status(self, post: Post):
        pass

    @abstractmethod
    def update_members(self, post: Post):
        pass
