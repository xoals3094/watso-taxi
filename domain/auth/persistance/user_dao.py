class MongoDBUserDao:
    def __init__(self, mongodb_connection):
        self.db = mongodb_connection['watso']

    def find_id_by_kakao_id(self, kakao_id) -> str | None:
        find = {
            'kakao.id': kakao_id
        }
        user_json = self.db.user.find_one(find)
        if user_json is None:
            return None
        return str(user_json['_id'])

    def create(self, nickname, profile_image_url, kakao_id) -> str:
        data = {
            'nickname': nickname,
            'profile_image_url': profile_image_url,
            'kakao': {
                'id': kakao_id
            }
        }

        id = self.db.user.insert_one(data)

        return str(id)
