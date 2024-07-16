from fastapi import Depends
import jwt
from config.setting import secret_key
from fastapi.security.api_key import APIKeyHeader
from exceptions import auth


oauth2_scheme = APIKeyHeader(name='Authorization')


def decode_token(token):
    try:
        payload = jwt.decode(token, secret_key, algorithms='HS256')
    except jwt.exceptions.ExpiredSignatureError:
        raise auth.TokenExpired(msg='만료된 토큰입니다')

    return payload


def get_user_id(token=Depends(oauth2_scheme)):
    data = decode_token(token)
    return int(data['id'])
