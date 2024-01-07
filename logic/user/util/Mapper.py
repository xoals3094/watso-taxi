from logic.auth.domain.User import User


class UserMapper:
    @staticmethod
    def mapping_user(user_json) -> User:
        user = User(id=user_json['_id'],
                    name=user_json['name'],
                    nickname=user_json['nickname'],
                    username=user_json['username'],
                    password=user_json['password'],
                    email=user_json['email'])

        return user
