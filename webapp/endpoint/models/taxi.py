from pydantic import BaseModel, Field
from datetime import datetime
from typing import List
from enum import Enum
from webapp.common.util.id_generator import create_id


class GroupQueryOption(str, Enum):
    JOINABLE = 'JOINABLE'
    JOINED = 'JOINED'


class Direction(str, Enum):
    STATION = 'STATION'
    CAMPUS = 'CAMPUS'


class TaxiGroupCreate(BaseModel):
    max_members: int = Field(..., description='최대 인원', examples=[4])
    departure_datetime: datetime = Field(..., description='출발 시간', examples=[datetime.now().strftime('%Y-%m-%dT%H:%M:%S')])
    direction: Direction


class GroupId(BaseModel):
    group_id: str = Field(..., description='생성된 게시글 ID', examples=[create_id()])


class SettleRequest(BaseModel):
    class Bill(BaseModel):
        user_id: str = Field(..., description='유저 ID', examples=[create_id()])
        cost: int = Field(..., description=' 비용', examples=[3000])

    fare: int = Field(..., description='비용', examples=[6200])
    bills: List[Bill] = None


class TaxiGroupDetail(BaseModel):
    class Fare(BaseModel):
        total: int = Field(..., description='총합', examples=['6200'])
        cost: int = Field(..., description='비용', examples=['3100'])

    class Member(BaseModel):
        current_members: int = Field(..., description='현재 인원', examples=[1])
        max_members: int = Field(..., description='최대 인원', examples=[4])

    id: str = Field(..., description='그룹 ID', examples=[create_id()])
    role: str = Field(..., description='권한', examples=['OWNER', 'MEMBER', 'NON_MEMBER'])
    status: str = Field(..., description='상태 코드', examples=['OPEN', 'CLOSE', 'SETTLE', 'COMPLETE'])
    direction: Direction
    departure_datetime: datetime = Field(..., description='출발 시간', examples=[datetime.now().strftime('%Y-%m-%dT%H:%M:%S')])
    fare: Fare
    member: Member

    @staticmethod
    def mapping(id, role, status, direction, departure_datetime, fare, cost, current_members, max_members):
        taxi_group = TaxiGroupDetail(
            id=id,
            role=role,
            status=status,
            direction=direction,
            departure_datetime=departure_datetime,
            fare=TaxiGroupDetail.Fare(
                total=fare,
                cost=cost
            ),
            member=TaxiGroupDetail.Member(
                current_members=current_members,
                max_members=max_members
            )
        )

        return taxi_group


class TaxiGroupSummary(BaseModel):
    class Fare(BaseModel):
        total: int = Field(..., description='총합', examples=['6200'])
        cost: int = Field(..., description='비용', examples=['3100'])

    class Member(BaseModel):
        current_members: int = Field(..., description='현재 인원', examples=[1])
        max_members: int = Field(..., description='최대 인원', examples=[4])

    id: str = Field(..., description='그룹 ID', examples=[create_id()])
    status: str = Field(..., description='상태 코드', examples=['OPEN', 'CLOSE', 'SETTLE', 'COMPLETE'])
    direction: Direction
    departure_datetime: datetime = Field(..., description='출발 시간', examples=[datetime.now().strftime('%Y-%m-%dT%H:%M:%S')])
    fare: Fare
    member: Member

    @staticmethod
    def mapping(id, status, direction, departure_datetime, fare, cost, current_members, max_members):
        taxi_group = TaxiGroupSummary(
            id=id,
            status=status,
            direction=direction,
            departure_datetime=departure_datetime,
            fare=TaxiGroupSummary.Fare(
                total=fare,
                cost=cost
            ),
            member=TaxiGroupSummary.Member(
                current_members=current_members,
                max_members=max_members
            )
        )

        return taxi_group


class FareDetail(BaseModel):
    class TaxiGroupMember(BaseModel):
        id: str = Field(..., description='유저 ID', examples=[create_id()])
        nickname: str = Field(..., description='닉네임', examples=['찰봉'])
        cost: int = Field(..., description='비용', examples=[3000])

    fare: int = Field(..., description='전체 비용', examples=[6000])
    members: List[TaxiGroupMember]

    @staticmethod
    def mapping(fare: int, members: list[(str, str, int)]):
        return FareDetail(
            fare=fare,
            members=[
                FareDetail.TaxiGroupMember(
                    id=id,
                    nickname=nickname,
                    cost=cost
                ) for id, nickname, cost in members
            ]
        )

