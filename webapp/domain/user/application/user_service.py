from webapp.domain.user.persistance.user_repository import UserRepository
from webapp.domain.user.entity.user import User
from webapp.endpoint.models.user import User as UserModel


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def register(self, nickname: str, profile_image_url: str) -> str:
        user = User.create(nickname, profile_image_url)
        self.user_repository.save(user)
        return user.id

    def get_user(self, user_id) -> UserModel:
        user = self.user_repository.find_by_id(user_id)

        return UserModel(
            id=user.id,
            nickname=user.nickname,
            profile_image_url=user.profile_image_url
        )
