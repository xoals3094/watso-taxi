from fastapi import Depends
from pydantic import BaseModel, Field
from datetime import datetime
from dependency_injector.wiring import inject, Provide
from typing import List
from src.taxi_container import TaxiContainer
from src.payment_container import PaymentContainer
from util.token_decoder import get_user_id

from query.taxi_group.taxi_group_query_dao import MySQLTaxiGroupQueryDao
from domain.payment.application.payment_service import PaymentService
from app.api.taxi_group.taxi_api import taxi_router


class OwnerModel(BaseModel):
    id: int = Field(..., description='유저 ID')
    nickname: str = Field(..., description='닉네임')

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'id': 1719843797268,
                    'nickname': '찰봉'
                }
            ]
        }
    }


class MemberModel(BaseModel):
    current_member: int = Field(..., description='현재 인원', examples=[1])
    max_member: int = Field(..., description='최대 인원', examples=[4])
    members: List[int] = Field(..., description='참여자 ID 목록', examples=[[1719843797268]])


class MemBerSummaryModel(BaseModel):
    current_member: int = Field(..., description='현재 인원', examples=[1])
    max_member: int = Field(..., description='최대 인원', examples=[4])


class ResponseTaxiGroupModel(BaseModel):
    id: int = Field(..., description='그룹 ID', examples=[1719843797268])
    owner: OwnerModel
    status: str = Field(..., description='상태 코드', examples=['OPEN'])
    direction: str = Field(..., description='방면', examples=['CAMPUS'])
    depart_datetime: datetime = Field(..., description='출발 시간', examples=[datetime.now().strftime('%Y-%m-%dT%H:%M:%S')])
    fee: int = Field(..., description='비용', examples=['6200'])
    member: MemberModel


class ResponseTaxiGroupSummaryModel(BaseModel):
    id: int = Field(..., description='그룹 ID', examples=[1719843797268])
    owner: OwnerModel
    status: str = Field(..., description='상태 코드', examples=['OPEN'])
    direction: str = Field(..., description='방면', examples=['CAMPUS'])
    depart_datetime: datetime = Field(..., description='출발 시간', examples=[datetime.now().strftime('%Y-%m-%dT%H:%M:%S')])
    fee: int = Field(..., description='비용', examples=['6200'])
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


@taxi_router.get('', response_model=List[ResponseTaxiGroupSummaryModel], tags=['taxi-query'])
@inject
async def get_taxi_groups(direction: str,
                          depart_datetime: datetime,
                          user_id: int = Depends(get_user_id),
                          group_query: MySQLTaxiGroupQueryDao = Depends(Provide[TaxiContainer.taxi_group_query_dao])):

    groups = group_query.find_groups(user_id, direction, depart_datetime)
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

