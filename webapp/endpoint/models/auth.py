from pydantic import BaseModel, Field


class AccessToken(BaseModel):
    access_token: str = Field(..., description='access_token', examples=['jwt token'])


class RefreshToken(BaseModel):
    refresh_token: str = Field(..., description='refresh token', examples=['jwt token'])


class LoginRequest(BaseModel):
    code: str = Field(..., description='카카오 인가 코드', examples=['kakao access token'])
    fcm_token: str = Field(..., description='device token', examples=['device token'])


class TokenPair(RefreshToken, AccessToken):
    pass
