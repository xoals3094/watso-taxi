from fastapi import Depends
from pydantic import BaseModel
from webapp.common.util.token_decoder import get_user_id
from webapp.domain.user.application.user_service import UserService
from webapp.common.src.user_container import UserContainer

from app.api.user.user_api import user_router


class ResponseUserModel(BaseModel):
    user_id: int
    nickname: str
    profile_image_url: str


@user_router.get('', response_model=ResponseUserModel, tags=['user'])
async def get_user(user_id: int = Depends(get_user_id),
                   user_service: UserService = Depends(UserContainer.user_service)):
    user = user_service.get_user(user_id)
    return user.json
