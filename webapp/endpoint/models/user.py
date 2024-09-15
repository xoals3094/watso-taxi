from pydantic import BaseModel


class User(BaseModel):
    id: str
    nickname: str
    profile_image_url: str
