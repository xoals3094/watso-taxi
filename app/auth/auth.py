from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from dependency_injector.wiring import inject, Provide
from logic.auth.application.port.incoming.AuthUseCase import AuthUseCase
from logic.auth.application.AuthService import JwtAuthService
from src.auth_container import AuthContainer

from app.util.error_handling import auth_error_handler, format_error

auth_router = APIRouter(prefix='/auth')

oauth = OAuth2PasswordBearer(tokenUrl='/auth/login')


class LogoutModel(BaseModel):
    access_token: str


class RefreshModel(BaseModel):
    refresh_token: str


@auth_router.post('/login')
@inject
async def login(req: OAuth2PasswordRequestForm = Depends(),
                auth_use_case: AuthUseCase = Depends(Provide[AuthContainer.auth_service])):
    """로그인"""
    access_token, refresh_token = auth_use_case.login(req.username, req.password)
    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
    }


@auth_router.post('/logout')
@inject
async def logout(req: LogoutModel, auth_use_case: AuthUseCase = Depends(Provide[AuthContainer.auth_service])):
    """로그아웃"""
    auth_use_case.logout(req.access_token)
    return '', 204


@auth_router.get('/refresh')
@inject
async def get(req: RefreshModel, jwt_auth_service: JwtAuthService = Depends(Provide[AuthContainer.auth_service])):
    """토큰 갱신"""
    access_token = jwt_auth_service.refresh(req.refresh_token)
    return {'access_token': access_token}


from logic.auth.application.KakaoLoginService import KakaoLoginService
@auth_router.post('/login/kakao/callback')
async def login_kakao_callback(code: str = None):
    kakao_login_service = KakaoLoginService()
    kakao_login_service.login(code)


# @auth_router.get('/test'):
# async def
