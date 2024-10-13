from dataclasses import dataclass
from datetime import datetime
from webapp.common.util.id_generator import create_id


@dataclass
class Base:
    @property
    def dict(self):
        result = {}
        for key, value in self.__dict__.items():
            result[key] = value
            if isinstance(value, list):
                result[key] = [item.__dict__ for item in value]
            elif isinstance(value, Base):
                result[key] = value.__dict__
        return result


@dataclass
class Chat(Base):
    id: str
    timestamp: str
    type: str = 'CHAT'

    @staticmethod
    def _create(cls, type, **kwargs):
        return cls(
            id=create_id(),
            type=type,
            timestamp=datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
            **kwargs
        )


@dataclass
class User(Base):
    id: str
    nickname: str
    profile_image_url: str


@dataclass
class Metadata(Chat):
    type: str = "METADATA"
    session_id: str = None
    users: list[User] = None
    chats: list[Chat] = None

    @classmethod
    def create(cls, session_id, users, chats):
        return Chat._create(cls, cls.type, session_id=session_id, users=users, chats=chats)


@dataclass
class Pending(Chat):
    type: str = "PENDING"
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
