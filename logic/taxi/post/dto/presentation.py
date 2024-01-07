from pydantic import BaseModel, Field
from datetime import datetime


class PlaceModel(BaseModel):
    depart_place: str = Field(description='출발지')
    arrive_place: str = Field(description='도착지')


class UserModel(BaseModel):
    id: int
    nickname: str


class PostWriteModel(BaseModel):
    direction: str
    depart_time: datetime
    max_member: int
    content: str


class PostUpdateModel(BaseModel):
    order_time: datetime
    place: str
    min_member: int
    max_member: int
