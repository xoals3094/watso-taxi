from abc import *


class UserIdFinder(metaclass=ABCMeta):
    @abstractmethod
    def find_user_id_by_comment_id(self, comment_id):
        pass

    @abstractmethod
    def find_user_id_by_post_id(self, post_id):
        pass
