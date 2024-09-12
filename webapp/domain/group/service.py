from abc import *


class GroupService(metaclass=ABCMeta):
    @abstractmethod
    def create(self, *args, **kwargs) -> int:
        pass

    @abstractmethod
    def open(self, group_id: int):
        pass

    @abstractmethod
    def close(self, group_id: int):
        pass

    @abstractmethod
    def participate(self, group_id: int, user_id: int):
        pass

    @abstractmethod
    def leave(self, group_id: int, user_id: int):
        pass
