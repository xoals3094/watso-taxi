from pydantic import BaseModel


class User(BaseModel):
    id: int
    nickname: str
    profile_image_url: str
