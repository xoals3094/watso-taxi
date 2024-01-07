from pydantic import BaseModel, validator
from app.util.validator import validate_name, validate_password, validate_username, validate_nickname, validate_account_number, validate_email


class SignupModel(BaseModel):
    auth_token: str
    name: str
    username: str
    pw: str
    nickname: str
    account_number: str
    email: str

    @validator('name')
    def _name(cls, v):
        validate_name(v)
        return v

    @validator('username')
    def _username(cls, v):
        validate_username(v)
        return v

    @validator('pw')
    def validate_password(cls, v):
        validate_password(v)
        return v

    @validator('nickname')
    def validate_nickname(cls, v):
        validate_nickname(v)
        return v

    @validator('account_number')
    def validate_account_number(cls, v):
        validate_account_number(v)
        return v

    @validator('email')
    def validate_email(cls, v):
        validate_email(v)
        return v
