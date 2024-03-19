from domain.auth.application.port.outgoing.UserDao import UserDao
from domain.auth.domain.User import User


class MongoDBUserDao(UserDao):
    def __init__(self, mongodb_connection):
        self.db = mongodb_connection['watso']

    def find_user_by_kakao_id(self, kakao_id) -> User | None:
        find = {
            'kakao.id': kakao_id
        }
        user_json = self.db.user.find_one(find)
        if user_json is None:
            return

        return User(id=str(user_json['_id']), nickname=user_json['nickname'], profile_image_url=user_json['profile_image_url'])

    def create(self, nickname, profile_image_url, kakao_id) -> User:
        data = {
            'nickname': nickname,
            'profile_image_url': profile_image_url,
            'kakao': {
                'id': kakao_id
            }
        }

        id = self.db.user.insert_one(data)

        return User(id=str(id), nickname=nickname, profile_image_url=nickname)
