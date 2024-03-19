from fastapi import APIRouter, Depends
from pydantic import BaseModel
from dependency_injector.wiring import inject, Provide
from src.auth_container import AuthContainer
from domain.auth.application.KakaoLoginService import KakaoLoginService


auth_router = APIRouter(prefix='/auth')


class LogoutModel(BaseModel):
    access_token: str


class RefreshModel(BaseModel):
    refresh_token: str


@auth_router.get('/kakao-login', tags=['auth'])
@inject
async def login(access_token: str, kakao_service: KakaoLoginService = Depends(Provide[AuthContainer.kakao_service])):
    """로그인"""
    access_token, refresh_token = kakao_service.login(access_token)
    return {
        'access_token': access_token,
        'refresh_token': refresh_token
    }


@auth_router.get('/login/kakao/callback', tags=['kakao'])
async def login_kakao_callback(code: str = None):
    return


