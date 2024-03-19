from abc import *
from domain.auth.domain.User import User


class UserDao(metaclass=ABCMeta):
    @abstractmethod
    def find_user_by_kakao_id(self, kakao_id) -> User | None:
        pass

    @abstractmethod
    def create(self, nickname, profile_image_url, kakao_id) -> User:
        pass
