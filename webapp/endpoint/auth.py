from fastapi import APIRouter, Depends, status
from webapp.domain.auth.application.jwt_auth_service import JWTAuthService
from webapp.domain.auth.application.kakao_auth_service import KakaoAuthService
from webapp.common.src import container

from .models.auth import (
    LoginRequest,
    TokenPair,
    RefreshToken,
    RefreshRequest
)


auth_router = APIRouter()


@auth_router.delete(
    '/logout',
    status_code=status.HTTP_204_NO_CONTENT
)
async def logout(
        req: RefreshToken,
        auth_service: JWTAuthService = Depends(container.get_jwt_auth_service)
) -> None:

    auth_service.logout(req.refresh_token)


@auth_router.post(
    '/login/refresh',
    response_model=TokenPair,
)
async def refresh(
        req: RefreshRequest,
        auth_service: JWTAuthService = Depends(container.get_jwt_auth_service)
) -> TokenPair:

    access_token, refresh_token = auth_service.refresh(req.refresh_token, req.fcm_token)
    return TokenPair(
        access_token=access_token,
        refresh_token=refresh_token
    )


@auth_router.post(
    '/login/kakao',
    response_model=TokenPair
)
async def kakao_login(
        req: LoginRequest,
        auth_service: KakaoAuthService = Depends(container.get_kakao_auth_service)
) -> TokenPair:

    access_token, refresh_token = auth_service.login(req.code, req.fcm_token)
    return TokenPair(
        access_token=access_token,
        refresh_token=refresh_token
    )
