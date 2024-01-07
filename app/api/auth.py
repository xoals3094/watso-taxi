from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
import jwt
from config.production.setting import secret_key

oauth = OAuth2PasswordBearer(tokenUrl='/auth/login')


def decode_token(token):
    payload = jwt.decode(token, secret_key, algorithms='HS256')
    return payload


def get_user_id(token: str = Depends(oauth)):
    data = decode_token(token)
    return data['user_id']
