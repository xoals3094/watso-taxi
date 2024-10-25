from sqlalchemy import select
from webapp.common.exceptions import persistence
from webapp.domain.user.entity.user import User
from webapp.domain.chat.chat import Entry, Exit


class ChatGroupProcessor:
    def __init__(self, channel_manager, session_context):
        self.channel_manager = channel_manager
        self.session_context = session_context

    def _get_user(self, user_id):
        with self.session_context() as session:
            stmt = select(User).filter_by(id=user_id)
            user = session.execute(stmt).scalar_one()

        return user.id, user.nickname, user.profile_image_url

    async def participate_process(self, user_id: str, group_id: str):
        try:
            channel = self.channel_manager.get_channel(group_id)
        except persistence.ResourceNotFound:
            channel = self.channel_manager.create_channel(group_id)

        user_id, nickname, profile_image_url = self._get_user(user_id)
        channel.cache_user(user_id=user_id, nickname=nickname, profile_image_url=profile_image_url)
        await channel.broadcast(
            Entry.create(
                user_id=user_id,
                nickname=nickname,
                profile_image_url=profile_image_url
            )
        )

    async def leave_process(self, user_id: str, group_id: str):
        try:
            channel = self.channel_manager.get_channel(group_id)
        except persistence.ResourceNotFound:
            channel = self.channel_manager.create_channel(group_id)

        await channel.broadcast(
            Exit.create(user_id=user_id)
        )
