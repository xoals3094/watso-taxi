from fastapi import APIRouter, Depends, status
from dependency_injector.wiring import inject, Provide

from webapp.domain.auth.application.kakao_login_service import KakaoLoginService
from webapp.domain.auth.application.jwt_login_service import JWTLoginService
from webapp.common.src.auth_container import AuthContainer

from .models.auth import (
    TokenPair,
    RefreshToken
)


auth_router = APIRouter(prefix='/auth')


@auth_router.delete(
    '/logout',
    status_code=status.HTTP_204_NO_CONTENT
)
@inject
async def logout(
        req: RefreshToken,
        jwt_login_service: JWTLoginService = Depends(Provide[AuthContainer.jwt_login_service])
):
    jwt_login_service.logout(req.refresh_token)


@auth_router.post(
    '/login/refresh',
    response_model=TokenPair,
)
@inject
async def refresh(
        req: RefreshToken,
        jwt_login_service: JWTLoginService = Depends(Provide[AuthContainer.jwt_login_service])
) -> TokenPair:
    access_token, refresh_token = jwt_login_service.refresh(req.refresh_token)

    return TokenPair(
        access_token=access_token,
        refresh_token=refresh_token
    )


@auth_router.get(
    '/login/kakao',
    response_model=TokenPair
)
@inject
async def kakao_login(
        access_token: str,
        kakao_service: KakaoLoginService = Depends(Provide[AuthContainer.kakao_service])
):
    access_token, refresh_token = kakao_service.login(access_token)
    return TokenPair(
        access_token=access_token,
        refresh_token=refresh_token
    )


@auth_router.get('/login/kakao/callback', include_in_schema=False)
async def login_kakao_callback(code: str = None):
    return


