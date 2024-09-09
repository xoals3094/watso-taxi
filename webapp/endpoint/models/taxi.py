from pydantic import BaseModel, Field
from datetime import datetime
from typing import List
from enum import Enum


class TaxiGroupCreate(BaseModel):
    max_members: int = Field(..., description='최대 인원', examples=[4])
    depart_datetime: datetime = Field(..., description='출발 시간', examples=[datetime.now().strftime('%Y-%m-%dT%H:%M:%S')])
    direction: str = Field(..., description='방면 코드', examples=['CAMPUS'])


class GroupId(BaseModel):
    group_id: int = Field(..., description='생성된 게시글 ID', examples=[1232415])


class FeeUpdate(BaseModel):
    class Bill(BaseModel):
        user_id: int = Field(..., description='유저 ID', examples=[1232415])
        cost: int = Field(..., description=' 비용', examples=[3000])

    fee: int = Field(..., description='비용', examples=[6200])
    bills: List[Bill]


class TaxiGroup(BaseModel):
    class Fee(BaseModel):
        total: int = Field(..., description='총합', examples=['6200'])
        cost: int = Field(..., description='비용', examples=['3100'])

    class Member(BaseModel):
        current_member: int = Field(..., description='현재 인원', examples=[1])
        max_member: int = Field(..., description='최대 인원', examples=[4])

    id: int = Field(..., description='그룹 ID', examples=[1719843797268])
    role: str = Field(..., description='권한', examples=['OWNER'])
    status: str = Field(..., description='상태 코드', examples=['OPEN'])
    direction: str = Field(..., description='방면', examples=['CAMPUS'])
    depart_datetime: datetime = Field(..., description='출발 시간', examples=[datetime.now().strftime('%Y-%m-%dT%H:%M:%S')])
    fee: Fee
    member: Member


class BillsDetail(BaseModel):
    class Bill(BaseModel):
        class User(BaseModel):
            id: int = Field(..., description='유저 ID', examples=[1719843797268])
            nickname: str = Field(..., description='닉네임', examples=['찰봉'])

        user: User
        cost: int = Field(..., description='비용', examples=[3000])

    fee: int = Field(..., description='전체 비용', examples=[6000])
    bills: List[Bill]


class ResponseURL(BaseModel):
    url: str = Field(..., description='정산 URL', examples=['https://qr.kakaopay.com/code'])


class GroupQueryOption(str, Enum):
    JOINABLE = 'JOINABLE'
    JOINED = 'JOINED'


class Direction(str, Enum):
    STATION = 'STATION'
    CAMPUS = 'CAMPUS'
