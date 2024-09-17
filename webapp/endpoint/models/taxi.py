from pydantic import BaseModel, Field
from datetime import datetime
from typing import List
from enum import Enum
from webapp.common.util.id_generator import create_id
from webapp.domain.taxi_group.entity.taxi_group import TaxiGroup as TaxiGroupDomain


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


class FareUpdate(BaseModel):
    class Member(BaseModel):
        id: str = Field(..., description='유저 ID', examples=[create_id()])
        cost: int = Field(..., description=' 비용', examples=[3000])

    fare: int = Field(..., description='비용', examples=[6200])
    members: List[Member]


class TaxiGroup(BaseModel):
    class Fare(BaseModel):
        fare: int = Field(..., description='총합', examples=['6200'])
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
    def mapping(user_id, taxi_group: TaxiGroupDomain):
        role = "OWNER" if taxi_group.owner_id == user_id else 'MEMBER'
        member = next((member for member in taxi_group.members if member.user_id == user_id), None)
        cost = taxi_group.fare // (len(taxi_group.members) + 1)
        if member:
            cost = member.cost

        taxi_group = TaxiGroup(
            id=taxi_group.id,
            role=role,
            status=taxi_group.status,
            direction=taxi_group.direction,
            departure_datetime=taxi_group.departure_datetime,
            fare=TaxiGroup.Fare(
                fare=taxi_group.fare,
                cost=cost
            ),
            member=TaxiGroup.Member(
                current_members=len(taxi_group.members),
                max_members=taxi_group.max_members
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

