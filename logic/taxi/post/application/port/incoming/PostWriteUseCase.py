from abc import *
from datetime import datetime


class PostWriteUseCase(metaclass=ABCMeta):
    @abstractmethod
    def create(self,
               owner_id: str,
               depart_point_id: str,
               arrive_point_id: str,
               depart_datetime: datetime,
               max_member: int,
               notice: str) -> str:
        pass

    @abstractmethod
    def delete(self, post_id, user_id):
        pass

    @abstractmethod
    def modify(self, user_id, post_id, notice):
        pass

    @abstractmethod
    def change_status(self, user_id, post_id, status):
        pass

    @abstractmethod
    def participate(self, user_id, post_id):
        pass

    @abstractmethod
    def leave(self, user_id, post_id):
        pass
