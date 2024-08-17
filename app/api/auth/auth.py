from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from dependency_injector.wiring import inject, Provide
from src.auth_container import AuthContainer
from domain.auth.application.kakao_login_service import KakaoLoginService
from domain.auth.application.jwt_login_service import JWTLoginService


auth_router = APIRouter(prefix='/auth')


class ResponseLoginModel(BaseModel):
    access_token: str = Field(..., description='access token', examples=['jwt token'])
    refresh_token: str = Field(..., description='refresh token', examples=['jwt token'])


class RequestRefreshModel(BaseModel):
    refresh_token: str = Field(..., description='refresh token', examples=['jwt token'])


@auth_router.delete('/logout', tags=['auth'])
@inject
async def logout(req: RequestRefreshModel, jwt_login_service: JWTLoginService = Depends(Provide[AuthContainer.jwt_login_service])):
    jwt_login_service.logout(req.refresh_token)


@auth_router.post('/login/refresh', response_model=ResponseLoginModel, tags=['auth'])
@inject
async def refresh(req: RequestRefreshModel, jwt_login_service: JWTLoginService = Depends(Provide[AuthContainer.jwt_login_service])):
    access_token, refresh_token = jwt_login_service.refresh(req.refresh_token)

    return {
        'access_token': access_token,
        'refresh_token': refresh_token
    }


@auth_router.get('/login/kakao', response_model=ResponseLoginModel, tags=['auth'])
@inject
async def kakao_login(access_token: str, kakao_service: KakaoLoginService = Depends(Provide[AuthContainer.kakao_service])):
    access_token, refresh_token = kakao_service.login(access_token)
    return {
        'access_token': access_token,
        'refresh_token': refresh_token
    }


@auth_router.get('/login/kakao/callback', include_in_schema=False)
async def login_kakao_callback(code: str = None):
    return


