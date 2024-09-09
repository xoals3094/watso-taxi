class ResponseUser:
    def __init__(self, user_id, nickname, profile_image_url):
        self.user_id = user_id
        self.nickname = nickname
        self.profile_image_url = profile_image_url

    @property
    def json(self):
        return {
            'user_id': self.user_id,
            'nickname': self.nickname,
            'profile_image_url': self.profile_image_url
        }
