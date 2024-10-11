from fastapi import WebSocket
from webapp.domain.chat.chat import Chat, Pended


class Session:
    def __init__(self, id, websocket: WebSocket):
        self.id = id
        self.websocket = websocket
        self.chat_queue: list[Chat] = []

    async def link(self, websocket: WebSocket):
        self.websocket = websocket
        pended = Pended.create(chats=self.chat_queue)
        await self.send(pended)
        self.chat_queue = []

    def unlink(self):
        self.websocket = None

    async def send(self, chat):
        if self.websocket is None:
            self.chat_queue.append(chat)
            # 알림 코드
            return

        await self.websocket.send_json(str(chat.__dict__))


class Channel:
    def __init__(self, group_id):
        self.group_id = group_id
        self.sessions: dict[str, Session] = {}

    async def connect(self, session_id: str, websocket: WebSocket):
        if session_id not in self.sessions:
            session = Session(id=session_id, websocket=websocket)
            self.sessions[session_id] = session
            return

        await self.sessions[session_id].link(websocket)

    def disconnect(self, session_id):
        self.sessions[session_id].unlink()

    async def broadcast(self, chat):
        for session in self.sessions.values():
            await session.send(chat)
