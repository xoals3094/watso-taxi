import jwt
from datetime import datetime, timedelta


def create_access_token():
    payload = {
        'id': 'f927fac8b27544d19c8e890140399040',
        #'exp': datetime.utcnow() + timedelta(minutes=30)
    }
    return jwt.encode(payload, 'dev')

print(create_access_token())
