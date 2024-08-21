from fastapi import Depends, Query
from pydantic import BaseModel, Field
from datetime import datetime
from dependency_injector.wiring import inject, Provide
from typing import List
from src.taxi_container import TaxiContainer
from src.payment_container import PaymentContainer
from util.token_decoder import get_user_id
from enum import Enum
from query.taxi_group.taxi_group_query_dao import MySQLTaxiGroupQueryDao
from domain.payment.application.payment_service import PaymentService
from app.api.taxi_group.taxi_api import taxi_router


class MemberModel(BaseModel):
    current_member: int = Field(..., description='현재 인원', examples=[1])
    max_member: int = Field(..., description='최대 인원', examples=[4])
    members: List[int] = Field(..., description='참여자 ID 목록', examples=[[1719843797268]])


class MemBerSummaryModel(BaseModel):
    current_member: int = Field(..., description='현재 인원', examples=[1])
    max_member: int = Field(..., description='최대 인원', examples=[4])


class ResponseFeeModel(BaseModel):
    total: int = Field(..., description='총합', examples=['6200'])
    cost: int = Field(..., description='비용', examples=['3100'])


class ResponseTaxiGroupModel(BaseModel):
    id: int = Field(..., description='그룹 ID', examples=[1719843797268])
    owner_id: int = Field(..., description='대표유저 ID', examples=[1719843797268])
    status: str = Field(..., description='상태 코드', examples=['OPEN'])
    direction: str = Field(..., description='방면', examples=['CAMPUS'])
    depart_datetime: datetime = Field(..., description='출발 시간', examples=[datetime.now().strftime('%Y-%m-%dT%H:%M:%S')])
    fee: int = Field(..., description='비용', examples=['6200'])
    member: MemberModel


class ResponseTaxiGroupSummaryModel(BaseModel):
    id: int = Field(..., description='그룹 ID', examples=[1719843797268])
    owner_id: int = Field(..., description='대표유저 ID', examples=[1719843797268])
    status: str = Field(..., description='상태 코드', examples=['OPEN'])
    direction: str = Field(..., description='방면', examples=['CAMPUS'])
    depart_datetime: datetime = Field(..., description='출발 시간', examples=[datetime.now().strftime('%Y-%m-%dT%H:%M:%S')])
    fee: ResponseFeeModel
    member: MemBerSummaryModel


class ResponseUser(BaseModel):
    id: int = Field(..., description='유저 ID', examples=[1719843797268])
    nickname: str = Field(..., description='닉네임', examples=['찰봉'])


class ResponseBill(BaseModel):
    user: ResponseUser
    cost: int = Field(..., description='비용', examples=[3000])


class ResponseBills(BaseModel):
    fee: int = Field(..., description='전체 비용', examples=[6000])
    bills: List[ResponseBill]


class ResponseURL(BaseModel):
    url: str = Field(..., description='정산 URL', examples=['https://qr.kakaopay.com/code'])


class GroupQueryOption(str, Enum):
    JOINABLE = 'JOINABLE'
    JOINED = 'JOINED'


class Direction(str, Enum):
    STATION = 'STATION'
    CAMPUS = 'CAMPUS'


@taxi_router.get('', response_model=List[ResponseTaxiGroupSummaryModel], tags=['taxi-query'])
@inject
async def get_taxi_groups(option: GroupQueryOption = Query(None, description='조회 옵션'),
                          direction: Direction = Query(None, description='조회할 방향'),
                          depart_datetime: datetime = None,
                          user_id: int = Depends(get_user_id),
                          group_query: MySQLTaxiGroupQueryDao = Depends(Provide[TaxiContainer.taxi_group_query_dao])):
    if option == GroupQueryOption.JOINABLE.value:
        groups = group_query.find_joinable_groups(user_id, direction, depart_datetime)

    elif option == GroupQueryOption.JOINED.value:
        groups = group_query.find_joined_groups(user_id)

    else:
        groups = group_query.find_complete_groups(user_id)

    return [group.json for group in groups]


@taxi_router.get('/{group_id}', response_model=ResponseTaxiGroupModel, tags=['taxi-query'])
@inject
async def get_taxi_group_detail(group_id: int,
                                group_query: MySQLTaxiGroupQueryDao = Depends(Provide[TaxiContainer.taxi_group_query_dao])):
    group = group_query.find_group(group_id)
    return group.json


@taxi_router.get('/{group_id}/fee', response_model=ResponseBills, tags=['taxi-query'])
@inject
async def get_bills(group_id: int,
                    group_query: MySQLTaxiGroupQueryDao = Depends(Provide[TaxiContainer.taxi_group_query_dao])):
    group = group_query.find_bills_by_group_id(group_id)
    return group.json


@taxi_router.get('/{group_id}/settle-code', response_model=ResponseURL, tags=['taxi-query'])
@inject
async def get_settlement_code(group_id: int,
                              user_id: int = Depends(get_user_id),
                              payment_service: PaymentService = Depends(Provide[PaymentContainer.payment_service])):
    url = payment_service.create_url(group_id, user_id)
    return {
        'url': url
    }

