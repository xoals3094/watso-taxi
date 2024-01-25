from fastapi import Depends
import jwt
from config.production.setting import secret_key
from fastapi.security.api_key import APIKeyHeader


oauth2_scheme = APIKeyHeader(name='Authorization')


def decode_token(token):
    payload = jwt.decode(token, secret_key, algorithms='HS256')
    return payload


def get_user_id(token=Depends(oauth2_scheme)):
    data = decode_token(token)
    return data['id']
