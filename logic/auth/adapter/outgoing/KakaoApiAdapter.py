from logic.auth.application.port.outgoing.KakaoDao import KakaoDao
from logic.auth.domain.KakaoUserInfo import KakaoUserInfo
import requests
from config.production import kakao


class ApiKakaoAdapter(KakaoDao):
    def get_token(self, authorization_code) -> (str, str):
        url = 'https://kauth.kakao.com/oauth/token'
        header = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {
            'grant_type': 'authorization_code',
            'client_id': kakao.client_id,
            'redirect_uri': kakao.redirect_uri,
            'code': authorization_code,
        }
        res = requests.post(url, headers=header, data=data)

        json = res.json()

        return json['access_token'], json['refresh_token']

    def get_user_info(self, access_token, refresh_token) -> KakaoUserInfo:
        url = 'https://kapi.kakao.com/v2/user/me'
        header = {
            'Content-type': 'application/x-www-form-urlencoded;charset=utf-8',
            'Authorization': f'Bearer ${access_token}'
        }

        res = requests.get(url, headers=header)
        json = res.json()
        kakao_account = json['kakao_account']

        return KakaoUserInfo(id=json['id'],
                             nickname=kakao_account['profile']['nickname'],
                             profile_image_url=kakao_account['profile']['profile_image_url'])

