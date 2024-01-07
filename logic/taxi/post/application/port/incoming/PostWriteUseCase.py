from abc import *
from logic.taxi.post.dto.presentation import PostWriteModel


class PostWriteUseCase(metaclass=ABCMeta):
    @abstractmethod
    def create(self, user_id, post: PostWriteModel) -> str:
        pass

    @abstractmethod
    def delete(self, post_id, handling_user_id):
        pass

    @abstractmethod
    def modify(self, user_id, post_id, patch_dict):
        pass

    @abstractmethod
    def change_status(self, user_id, post_id, status):
        pass

    @abstractmethod
    def join(self, post_id, user_id, nickname, order_json):
        pass

    @abstractmethod
    def quit(self, post_id, user_id):
        pass
