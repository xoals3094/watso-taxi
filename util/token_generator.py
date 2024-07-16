import jwt
from datetime import datetime, timedelta
from config.setting import secret_key


def create_access_token(user_id):
    payload = {
        'id': str(user_id),
        'exp': datetime.utcnow() + timedelta(minutes=30)
    }
    return jwt.encode(payload, secret_key)


def create_refresh_token():
    payload = {
        'exp': datetime.utcnow() + timedelta(days=90)
    }
    return jwt.encode(payload, secret_key)
