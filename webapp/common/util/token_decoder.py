import jwt
from datetime import datetime
from fastapi import Depends
from fastapi.security.api_key import APIKeyHeader
from config.setting import secret_key
from webapp.common.exceptions import auth

oauth2_scheme = APIKeyHeader(name='Authorization')


def decode_token(token):
    try:
        payload = jwt.decode(token, secret_key, algorithms='HS256')
    except jwt.exceptions.ExpiredSignatureError:
        raise auth.TokenExpired(msg='만료된 토큰입니다')

    return payload


def get_token_id_and_exp(token) -> (str, datetime):
    payload = decode_token(token)
    token_id = payload['token_id']
    exp = payload['exp']
    exp = datetime.fromtimestamp(exp)
    return token_id, exp


def get_user_id(token=Depends(oauth2_scheme)):
    data = decode_token(token)
    return data['id']
