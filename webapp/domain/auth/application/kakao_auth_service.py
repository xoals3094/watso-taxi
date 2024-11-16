from webapp.common.exceptions import persistence
from webapp.domain.user.application.user_service import UserService
from webapp.domain.auth.dto.kakao_user_info import KakaoUserInfo
from webapp.domain.auth.application.jwt_auth_service import JWTAuthService
from webapp.domain.auth.entity.kakao import Kakao
from webapp.domain.auth.persistance.kakao_repository import KakaoRepository
from webapp.domain.user.persistance.device_repository import DeviceRepository
from webapp.domain.user.entity.device import Device

from webapp.domain.auth.third_party import kakao_login_client


class KakaoAuthService:
    def __init__(
            self,
            user_service: UserService,
            jwt_auth_service: JWTAuthService,
            kakao_repository: KakaoRepository,
            device_repository: DeviceRepository
    ):
        self.user_service = user_service
        self.jwt_auth_service = jwt_auth_service
        self.kakao_repository = kakao_repository
        self.device_repository = device_repository

    def _register(self, kakao_user_info: KakaoUserInfo) -> str:
        user_id = self.user_service.register(
            nickname=kakao_user_info.nickname,
            profile_image_url=kakao_user_info.profile_image_url
        )

        return user_id

    def login(self, access_token, fcm_token) -> (str, str):
        kakao_user_info = kakao_login_client.get_user_info(access_token)
        try:
            kakao = self.kakao_repository.find_by_id(kakao_id=kakao_user_info.id)
        except persistence.ResourceNotFound:
            user_id = self._register(kakao_user_info)
            kakao = Kakao.create(
                user_id=user_id,
                kakao_id=kakao_user_info.id,
            )
            device = Device.create(user_id, fcm_token)
            self.kakao_repository.save(kakao)
            self.device_repository.save(device)

        return self.jwt_auth_service.login(kakao.user_id)
