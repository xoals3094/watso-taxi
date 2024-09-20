from fastapi import WebSocket
from sqlalchemy import select
from webapp.common.exceptions import persistence
from webapp.domain.chat.channel_manager import ChannelManager
from webapp.domain.chat.chat import Message, Entry, Exit, MetaData
from webapp.domain.user.entity.user import User as UserTable


class ChatService:
    def __init__(self, channel_manager: ChannelManager, session_context):
        self.session_context = session_context
        self.channel_manager = channel_manager

    async def participate(self, group_id: str, user_id, websocket: WebSocket):
        try:
            channel = self.channel_manager.get_channel(group_id)
        except persistence.ResourceNotFound:
            channel = self.channel_manager.create_channel(group_id)

        with self.session_context() as session:
            stmt = select(UserTable).filter_by(id=user_id)
            result = session.execute(stmt).scalar_one()
            entry = Entry.create(
                user_id=user_id,
                nickname=result.nickname,
                profile_image_url=result.profile_image_url
            )

            stmt = select(UserTable).filter(UserTable.id.in_(channel.member_ids))
            result = session.execute(stmt).scalars().all()
            meta_data = MetaData.create(
                users=[
                    {
                        'id': row.id,
                        'nickname': row.nickname,
                        'profile_image_url': row.profile_image_url
                    } for row in result
                ]
            )
        channel.join(user_id, websocket)
        await websocket.send_json(str(meta_data))
        await channel.send(entry)

    async def leave(self, group_id: str, user_id):
        channel = self.channel_manager.get_channel(group_id)
        channel.quit(user_id)
        chat = Exit.create(user_id)
        await channel.send(chat)

    async def send_message(self, group_id: str, user_id: str, content: str):
        channel = self.channel_manager.get_channel(group_id)
        message = Message.create(user_id, content)
        await channel.send(message)
