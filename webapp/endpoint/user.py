from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide

from webapp.common.util.token_decoder import get_user_id
from webapp.domain.user.application.user_service import UserService
from webapp.common.src.user_container import UserContainer
from webapp.endpoint.models.user import User


user_router = APIRouter()


@user_router.get('', response_model=User)
@inject
async def get_user(
        user_id: int = Depends(get_user_id),
        user_service: UserService = Depends(Provide[UserContainer.user_service])
) -> User:
    user = user_service.get_user(user_id)
    return user
