from fastapi import WebSocket
from webapp.common.util.id_generator import create_id
from webapp.domain.chat.chat import Chat, Pending, Metadata, User


class Session:
    def __init__(self, user_id, websocket: WebSocket):
        self.id = create_id()
        self.user_id = user_id
        self.websocket: WebSocket = websocket
        self.pending_chats: list[Chat] = []

    async def link(self, websocket: WebSocket):
        self.websocket = websocket
        pending = Pending.create(chats=self.pending_chats)
        await self.send(pending)
        self.pending_chats = []

    def unlink(self):
        self.websocket = None

    async def send(self, chat):
        if self.websocket is None:
            self.pending_chats.append(chat)
            # 알림 코드
            return

        await self.websocket.send_json(chat.dict)


class Channel:
    def __init__(self, group_id):
        self.group_id = group_id
        self.chats = []
        self.users = []
        self.sessions: dict[str, Session] = {}

    def cache_user(self, user_id, nickname, profile_image_url):
        user = User(
            id=user_id,
            nickname=nickname,
            profile_image_url=profile_image_url
        )
        self.users.append(user)

    async def connect(self, session_id: str, user_id: str, websocket: WebSocket):
        if session_id not in self.sessions:
            session = Session(user_id, websocket)
            self.sessions[session.id] = session
            metadata = Metadata.create(
                session_id=session.id,
                users=self.users,
                chats=self.chats
            )
            await session.send(metadata)
            return

        await self.sessions[session_id].link(websocket)

    def disconnect(self, session_id):
        self.sessions[session_id].unlink()

    async def broadcast(self, chat):
        self.chats.append(chat)
        for session in self.sessions.values():
            await session.send(chat)
