from fastapi import APIRouter, Depends, status
from dependency_injector.wiring import inject, Provide

from webapp.domain.auth.application.auth_service import AuthService
from webapp.common.src.auth_container import AuthContainer

from .models.auth import (
    TokenPair,
    RefreshToken
)


auth_router = APIRouter()


@auth_router.delete(
    '/logout',
    status_code=status.HTTP_204_NO_CONTENT
)
@inject
async def logout(
        req: RefreshToken,
        auth_service: AuthService = Depends(Provide[AuthContainer.auth_service])
) -> None:

    auth_service.logout(req.refresh_token)


@auth_router.post(
    '/login/refresh',
    response_model=TokenPair,
)
@inject
async def refresh(
        req: RefreshToken,
        auth_service: AuthService = Depends(Provide[AuthContainer.auth_service])
) -> TokenPair:

    access_token, refresh_token = auth_service.refresh(req.refresh_token)
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
        code: str,
        auth_service: AuthService = Depends(Provide[AuthContainer.auth_service])
) -> TokenPair:

    access_token, refresh_token = auth_service.login(code)
    return TokenPair(
        access_token=access_token,
        refresh_token=refresh_token
    )
