import jwt
from datetime import datetime, timedelta


def create_access_token():
    payload = {
        'id': 1723380608744,
        #'exp': datetime.utcnow() + timedelta(minutes=30)
    }
    return jwt.encode(payload, 'dev')

print(create_access_token())
