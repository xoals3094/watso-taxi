class User:
    def __init__(self, id, nickname, profile_image_url):
        self.id = id
        self.nickname = nickname
        self.profile_image_url = profile_image_url

    @property
    def json(self):
        return {
            'id': self.id,
            'nickname': self.nickname,
            'profile_image_url': self.profile_image_url
        }
