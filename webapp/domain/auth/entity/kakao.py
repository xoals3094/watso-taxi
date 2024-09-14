from datetime import datetime
from webapp.common.schema.models import KakaoModel
from webapp.common.util.id_generator import create_id


class Kakao(KakaoModel):
    @staticmethod
    def create(
            kakao_id: int,
            nickname: str,
            profile_image_url: str
    ):

        return Kakao(
            id=create_id(),
            kakao_id=kakao_id,
            nickname=nickname,
            profile_image_url=profile_image_url,
            created_at=datetime.now()
        )
