from pydantic import BaseModel, Field


class AccessToken(BaseModel):
    access_token: str = Field(..., description='access_token', examples=['jwt token'])


class RefreshToken(BaseModel):
    refresh_token: str = Field(..., description='refresh token', examples=['jwt token'])


class TokenPair(RefreshToken, AccessToken):
    pass
