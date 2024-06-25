from .taxi_group_api import taxi_group_router
from fastapi import Depends
from pydantic import BaseModel, Field
from datetime import datetime
from dependency_injector.wiring import inject, Provide
from typing import List
from src.taxi_container import TaxiContainer
from app.util.token_decoder import get_user_id

from domain.taxi_group.persistance.mysql_taxi_group_query_dao import MySQLTaxiGroupQueryDao


class OwnerModel(BaseModel):
    id: str = Field(..., description='유저 ID', examples=['ObjectId'])
    nickname: str = Field(..., description='닉네임', examples=['찰봉'])


class LocationModel(BaseModel):
    id: str = Field(..., description='포인트 ID', examples=['ObjectId'])
    name: str = Field(..., description='포인트 이름', examples=['부산대학교 밀양캠퍼스'])


class LocationsModel(BaseModel):
    depart_location: LocationModel
    arrive_location: LocationModel


class MemberModel(BaseModel):
    current_member: int = Field(..., description='현재 인원', examples=[3])
    max_member: int = Field(..., description='최대 인원', examples=[4])
    members: List[str] = Field(..., description='참여자 ID 목록', examples=[['ObjectId']])


class ResponseTaxiGroupModel(BaseModel):
    id: str = Field(..., description='그룹 ID', examples=['654601bf3d9ff6479fcdabcd'])
    owner: OwnerModel
    location: LocationsModel
    depart_datetime: datetime = Field(..., description='출발 시간', examples=[datetime.now()])
    fee: int = Field(..., description='비용', examples=['6200'])
    member: MemberModel


@taxi_group_router.get('', response_model=List[LocationModel], tags=['taxi-group-query'])
@inject
async def get_locations(taxi_group_query_dao: MySQLTaxiGroupQueryDao = Depends(Provide[TaxiContainer.point_query_dao])):
    locations = taxi_group_query_dao.find_locations()
    return [location.json for location in locations]


@taxi_group_router.get('', response_model=List[ResponseTaxiGroupModel], tags=['taxi-group-query'])
@inject
async def get_taxi_groups(depart_location_id: str,
                          arrive_location_id: str,
                          depart_datetime: datetime,
                          user_id: str = Depends(get_user_id),
                          group_query: MySQLTaxiGroupQueryDao = Depends(Provide[TaxiContainer.group_query_dao])):

    groups = group_query.find_groups(user_id, depart_location_id, arrive_location_id, depart_datetime)
    return [group.json for group in groups]


@taxi_group_router.get('/{group_id}', response_model=ResponseTaxiGroupModel, tags=['taxi-group-query'])
@inject
async def get_taxi_group_detail(group_id: str,
                                group_query: MySQLTaxiGroupQueryDao = Depends(Provide[TaxiContainer.group_query_dao])):
    group = group_query.find_group_by_id(group_id)
    return group.json
