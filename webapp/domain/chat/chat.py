from dataclasses import dataclass
from datetime import datetime
from webapp.common.util.id_generator import create_id


@dataclass
class Chat:
    id: str
    timestamp: datetime
    type: str = 'CHAT'

    @staticmethod
    def _create(cls, type, **kwargs):
        return cls(
            id=create_id(),
            type=type,
            timestamp=datetime.now(),
            **kwargs
        )


@dataclass
class Pended(Chat):
    type: str = "PENDED"
    chats: list[Chat] = None

    @classmethod
    def create(cls, chats):
        return Chat._create(cls, cls.type, chats=chats)


@dataclass
class Message(Chat):
    user_id: str = None
    content: str = None
    type: str = "MESSAGE"

    @classmethod
    def create(cls, user_id, content):
        return Chat._create(cls, cls.type, user_id=user_id, content=content)


@dataclass
class Entry(Chat):
    user: dict = None
    type: str = "ENTRY"

    @classmethod
    def create(cls, user_id, nickname, profile_image_url):
        user = dict(id=user_id, nickname=nickname, profile_image_url=profile_image_url)
        return Chat._create(cls, cls.type, user=user)


@dataclass
class Exit(Chat):
    user_id: str = None
    type: str = "EXIT"

    @classmethod
    def create(cls, user_id):
        return Chat._create(cls, cls.type, user_id=user_id)
