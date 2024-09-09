from pydantic import BaseModel, Field


class AccessToken(BaseModel):
    refresh_token: str = Field(..., description='refresh token', examples=['jwt token'])


class RefreshToken(BaseModel):
    refresh_token: str = Field(..., description='refresh token', examples=['jwt token'])


class TokenPair(AccessToken, RefreshToken):
    access_token: str = Field(..., description='access token', examples=['jwt token'])
    refresh_token: str = Field(..., description='refresh token', examples=['jwt token'])


