from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from dependency_injector.wiring import inject, Provide
from logic.auth.application.port.incoming.AuthUseCase import AuthUseCase
from logic.auth.application.AuthService import JwtAuthService
from src.auth_container import AuthContainer


auth_router = APIRouter(prefix='/auth')


