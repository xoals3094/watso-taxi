from abc import *
from logic.auth.domain.KakaoUserInfo import KakaoUserInfo


class KakaoDao(metaclass=ABCMeta):
    # @abstractmethod
    # def get_token(self, authorization_code) -> (str, str):
    #     pass

    @abstractmethod
    def get_user_info(self, access_token) -> KakaoUserInfo:
        pass
