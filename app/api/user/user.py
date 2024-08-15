from fastapi import Depends, Query
from pydantic import BaseModel, Field
from dependency_injector.wiring import inject, Provide
from util.token_decoder import get_user_id
from domain.user.application.user_service import UserService
from src.user_container import UserContainer

from app.api.user.user_api import user_router


class ResponseUserModel(BaseModel):
    user_id: int
    nickname: str
    profile_image_url: str


@user_router.get('', response_model=ResponseUserModel, tags=['user'])
@inject
async def get_user(user_id: int = Depends(get_user_id),
                   user_service: UserService = Depends(Provide[UserContainer.user_service])):
    user = user_service.get_user(user_id)
    return user.json
