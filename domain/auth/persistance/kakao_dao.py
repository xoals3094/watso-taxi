from domain.auth.dto.kakao_user_info import KakaoUserInfo
import requests


class ApiKakaoDao:
    def get_user_info(self, access_token) -> KakaoUserInfo:
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

