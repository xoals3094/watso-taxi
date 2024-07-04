from fastapi import Depends, status
from .taxi_api import taxi_router
from datetime import datetime
from typing import List

from pydantic import BaseModel, Field
from dependency_injector.wiring import inject, Provide

from domain.group.application.group_service import GroupService
from domain.taxi_group.application.taxi_group_service import TaxiGroupService
from domain.taxi_group.entity.bill import Bill
from src.taxi_container import TaxiContainer
from util.token_decoder import get_user_id


class RequestCreateGroupModel(BaseModel):
    max_member: int = Field(..., description='최대 인원', examples=[4])
    depart_datetime: datetime = Field(..., description='출발 시간', examples=[datetime.now()]),
    direction: str = Field(..., description='방면 코드', examples=['CAMPUS', 'STATION'])


class ResponseCreateGroupModel(BaseModel):
    group_id: int = Field(..., description='생성된 게시글 ID', examples=[1232415])


class RequestCharge(BaseModel):
    user_id: int = Field(..., description='유저 ID', examples=[1232415])
    cost: int = Field(..., description=' 비용', examples=[3000])


class RequestSettleModel(BaseModel):
    bills: List[RequestCharge]


@taxi_router.post('', status_code=status.HTTP_201_CREATED, tags=['taxi'])
@inject
async def create_taxi_group(req: RequestCreateGroupModel,
                            user_id=Depends(get_user_id),
                            taxi_group_service: TaxiGroupService = Depends(Provide[TaxiContainer.taxi_group_service])):
    taxi_group_service.create(owner_id=user_id,
                              max_member=req.max_member,
                              depart_datetime=req.depart_datetime,
                              direction=req.direction)


@taxi_router.patch('/{group_id}/open', status_code=status.HTTP_204_NO_CONTENT, tags=['taxi'])
@inject
async def recruit_group(group_id: int,
                        user_id=Depends(get_user_id),
                        taxi_group_service: TaxiGroupService = Depends(Provide[TaxiContainer.taxi_group_service])):
    taxi_group_service.recruit(group_id)


@taxi_router.patch('/{group_id}/close', status_code=status.HTTP_204_NO_CONTENT, tags=['taxi'])
@inject
async def close_group(group_id: int,
                      user_id=Depends(get_user_id),
                      taxi_group_service: TaxiGroupService = Depends(Provide[TaxiContainer.taxi_group_service])):
    taxi_group_service.close(group_id)


@taxi_router.patch('/{group_id}/settle', status_code=status.HTTP_204_NO_CONTENT, tags=['taxi'])
@inject
async def settle(group_id: int,
                 req: RequestSettleModel,
                 user_id=Depends(get_user_id),
                 taxi_group_service: TaxiGroupService = Depends(Provide[TaxiContainer.taxi_group_service])):
    datas = [(charge.user_id, charge.cost) for charge in req.bills]
    bill = Bill.mapping(datas)
    taxi_group_service.settle(group_id, bill)


@taxi_router.patch('/{group_id}/complete', status_code=status.HTTP_204_NO_CONTENT, tags=['taxi'])
@inject
async def complete(group_id: int,
                   user_id=Depends(get_user_id),
                   taxi_group_service: TaxiGroupService = Depends(Provide[TaxiContainer.group_service])):
    taxi_group_service.complete(group_id)


@taxi_router.post('/{group_id}/member', status_code=204, tags=['taxi'])
@inject
async def participate(group_id: int,
                      user_id: int = Depends(get_user_id),
                      group_service: GroupService = Depends(Provide[TaxiContainer.group_service])):
    group_service.participate(group_id, user_id)


@taxi_router.delete('/{group_id}/member', status_code=204, tags=['taxi'])
@inject
async def leave(group_id: int,
                user_id: int = Depends(get_user_id),
                group_service: GroupService = Depends(Provide[TaxiContainer.group_service])):
    group_service.leave(group_id, user_id)
