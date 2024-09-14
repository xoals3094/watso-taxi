from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Factory, Resource

from webapp.common import database
from webapp.domain.user.persistance.user_repository import UserRepository
from webapp.domain.user.application.user_service import UserService


class UserContainer(DeclarativeContainer):
    wiring_config = WiringConfiguration(modules=['webapp.endpoint.user'])

    session = Resource(database.get_session)

    user_repository = Factory(UserRepository, session=session)
    user_service = Factory(UserService, user_repository=user_repository)
