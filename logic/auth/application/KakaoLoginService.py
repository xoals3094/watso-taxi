import requests
from config.production import kakao


class KakaoLoginService:
    def login(self, code):
        url = 'https://kauth.kakao.com/oauth/token'
        header = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {
            'grant_type': 'authorization_code',
            'client_id': kakao.client_id,
            'redirect_uri': kakao.redirect_uri,
            'code': code,
        }
        res = requests.post(url, headers=header, data=data)

        print(res.json())