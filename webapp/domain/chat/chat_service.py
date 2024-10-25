from fastapi import WebSocket
from webapp.common.exceptions import persistence
from webapp.domain.chat.channel_manager import ChannelManager
from webapp.common.util.id_generator import create_id
from webapp.domain.chat.chat import Message


class ChatService:
    def __init__(self, channel_manager: ChannelManager):
        self.channel_manager = channel_manager

    async def connect(
            self,
            group_id: str,
            user_id: str,
            session_id: str | None,
            websocket: WebSocket
    ):
        try:
            channel = self.channel_manager.get_channel(group_id)
        except persistence.ResourceNotFound:
            channel = self.channel_manager.create_channel(group_id)

        if session_id is None:
            session_id = create_id()
        await channel.connect(user_id=user_id, session_id=session_id, websocket=websocket)

    async def disconnect(self, group_id: str, session_id: str):
        channel = self.channel_manager.get_channel(group_id)
        channel.disconnect(session_id)

    async def send_message(self, group_id: str, user_id: str, content: str):
        channel = self.channel_manager.get_channel(group_id)
        message = Message.create(user_id, content)
        await channel.broadcast(message)
