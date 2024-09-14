from webapp.domain.user.persistance.user_repository import UserRepository
from webapp.endpoint.models.user import User


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def get_user(self, user_id) -> User:
        user = self.user_repository.find_by_id(user_id)

        return User(
            id=user.id,
            nickname=user.nickname,
            profile_image_url=user.profile_image_url
        )
