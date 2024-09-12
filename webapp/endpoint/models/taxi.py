from pydantic import BaseModel, Field
from datetime import datetime
from typing import List
from enum import Enum


class GroupQueryOption(str, Enum):
    JOINABLE = 'JOINABLE'
    JOINED = 'JOINED'
    COMPLETED = 'COMPLETED'


class Direction(str, Enum):
    STATION = 'STATION'
    CAMPUS = 'CAMPUS'
    ALL = 'ALL'


class TaxiGroupCreate(BaseModel):
    max_members: int = Field(..., description='최대 인원', examples=[4])
    departure_datetime: datetime = Field(..., description='출발 시간', examples=[datetime.now().strftime('%Y-%m-%dT%H:%M:%S')])
    direction: Direction


class GroupId(BaseModel):
    group_id: int = Field(..., description='생성된 게시글 ID', examples=[1232415])


class FareUpdate(BaseModel):
    class Member(BaseModel):
        id: int = Field(..., description='유저 ID', examples=[1232415])
        cost: int = Field(..., description=' 비용', examples=[3000])

    fare: int = Field(..., description='비용', examples=[6200])
    members: List[Member]


class TaxiGroup(BaseModel):
    class Fare(BaseModel):
        total: int = Field(..., description='총합', examples=['6200'])
        cost: int = Field(..., description='비용', examples=['3100'])

    class Member(BaseModel):
        current_member: int = Field(..., description='현재 인원', examples=[1])
        max_member: int = Field(..., description='최대 인원', examples=[4])

    id: int = Field(..., description='그룹 ID', examples=[1719843797268])
    role: str = Field(..., description='권한', examples=['OWNER', 'NORMAL'])
    status: str = Field(..., description='상태 코드', examples=['OPEN', 'CLOSE', 'SETTLE', 'COMPLETE'])
    direction: Direction
    departure_datetime: datetime = Field(..., description='출발 시간', examples=[datetime.now().strftime('%Y-%m-%dT%H:%M:%S')])
    fare: Fare
    member: Member


class FareDetail(BaseModel):
    class TaxiMember(BaseModel):
        id: int = Field(..., description='유저 ID', examples=[1719843797268])
        nickname: str = Field(..., description='닉네임', examples=['찰봉'])
        cost: int = Field(..., description='비용', examples=[3000])

    fare: int = Field(..., description='전체 비용', examples=[6000])
    members: List[TaxiMember]
