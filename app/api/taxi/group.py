from fastapi import APIRouter, Depends, status, Response
from pydantic import BaseModel, Field
from datetime import datetime
from dependency_injector.wiring import inject, Provide
from typing import List

from domain.taxi.group.application.group_service import GroupService
from domain.taxi.group.persistance.group_query_dao import MongoDBGroupQueryDao
from domain.taxi.group.core.status import Status
from src.taxi_container import TaxiContainer

from app.util.token_decoder import get_user_id

post_router = APIRouter(prefix='/group')


class RequestCreateGroupModel(BaseModel):
    depart_point_id: str = Field(..., description='출발 지점 ID', examples=['ObjectId'])
    arrive_point_id: str = Field(..., description='도착 지점 ID', examples=['ObjectId'])
    depart_datetime: datetime = Field(..., description='출발 시간', examples=[datetime.now()])
    max_member: int = Field(..., description='최대 인원', examples=[3])
    notice: str = Field(..., description='공지사항', examples=['기숙사에서 내리지만 장소 협의 가능합니다'])


class ResponseCreateGroupModel(BaseModel):
    post_id: str = Field(..., description='생성된 게시글 ID', examples=['ObjectId'])


class OwnerModel(BaseModel):
    id: str = Field(..., description='유저 ID', examples=['ObjectId'])
    nickname: str = Field(..., description='닉네임', examples=['찰봉'])


class PointModel(BaseModel):
    id: str = Field(..., description='포인트 ID', examples=['ObjectId'])
    name: str = Field(..., description='포인트 이름', examples=['부산대학교 밀양캠퍼스'])


class PointsModel(BaseModel):
    depart_point: PointModel
    arrive_point: PointModel


class MemberModel(BaseModel):
    current_member: int = Field(..., description='현재 인원', examples=[3])
    max_member: int = Field(..., description='최대 인원', examples=[4])


class ResponseGroupListModel(BaseModel):
    id: str = Field(..., description='그룹 ID', examples=['654601bf3d9ff6479fcdabcd'])
    owner: OwnerModel
    point: PointsModel
    depart_datetime: datetime = Field(..., description='출발 시간', examples=[datetime.now()])
    fee: int = Field(..., description='비용', examples=['6200'])
    member: MemberModel


class MemberDetailModel(BaseModel):
    current_member: int = Field(..., description='현재 인원', examples=[3])
    max_member: int = Field(..., description='최대 인원', examples=[4])
    members: List[str] = Field(..., description='참여자 ID 목록', examples=[['ObjectId']])


class ResponseGroupDetailModel(BaseModel):
    id: str = Field(..., description='그룹 ID', examples=['654601bf3d9ff6479fcdabcd'])
    owner: OwnerModel
    point: PointsModel
    depart_datetime: datetime = Field(..., description='출발 시간', examples=[datetime.now()])
    status: str
    fee: int = Field(..., description='비용', examples=['6200'])
    notice: str = Field(..., description='공지사항', examples=['제가 쏩니다'])
    member: MemberDetailModel


class RequestModifyModel(BaseModel):
    notice: str = Field(..., description='공지사항', examples=['이것은 공지사항입니다'])


class RequestChangeStatusModel(BaseModel):
    status: str = Field(..., description='상태코드', examples=['RECRUITING', 'CLOSED', 'BOARDING', 'SETTLEMENT', 'COMPLETED'])


@post_router.get('', response_model=List[ResponseGroupListModel], tags=['group'])
@inject
async def get_posts(depart_point_id: str,
                    arrive_point_id: str,
                    depart_datetime: datetime,
                    user_id: str = Depends(get_user_id),
                    group_query: MongoDBGroupQueryDao = Depends(Provide[TaxiContainer.group_query_dao])):

    groups = group_query.find_groups(user_id, depart_point_id, arrive_point_id, depart_datetime)
    return [group.json for group in groups]


@post_router.post('', status_code=201, response_model=ResponseCreateGroupModel, tags=['group'])
@inject
async def create_group(req: RequestCreateGroupModel,
                       user_id: str = Depends(get_user_id),
                       group_service: GroupService = Depends(Provide[TaxiContainer.group_service])):

    group_id = group_service.create(owner_id=user_id,
                                    depart_point_id=req.depart_point_id,
                                    arrive_point_id=req.arrive_point_id,
                                    depart_datetime=req.depart_datetime,
                                    max_member=req.max_member,
                                    notice=req.notice)
    return {'group_id': group_id}


@post_router.get('/{group_id}', response_model=ResponseGroupDetailModel, tags=['group'])
@inject
async def get_group_detail(group_id: str,
                           group_query: MongoDBGroupQueryDao = Depends(Provide[TaxiContainer.group_query_dao])):
    group = group_query.find_group_by_id(group_id)
    return group.json


@post_router.patch('/{group_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['group'])
@inject
async def patch_post(req: RequestModifyModel,
                     group_id: str,
                     user_id: str = Depends(get_user_id),
                     group_service: GroupService = Depends(Provide[TaxiContainer.group_service])):
    group_service.modify_notice(user_id, group_id, req.notice)


@post_router.patch('/{group_id}/status', status_code=204, tags=['group'])
@inject
async def update_status(req: RequestChangeStatusModel,
                        group_id: str,
                        user_id: str = Depends(get_user_id),
                        group_service: GroupService = Depends(Provide[TaxiContainer.group_service])):
    group_service.change_status(user_id, group_id, Status(req.status))


@post_router.post('/{group_id}/member', status_code=204, tags=['group'])
@inject
async def participate(group_id: str,
                      user_id: str = Depends(get_user_id),
                      group_service: GroupService = Depends(Provide[TaxiContainer.group_service])):
    group_service.participate(user_id, group_id)


@post_router.delete('/{group_id}/member', status_code=204, tags=['group'])
@inject
async def leave(group_id: str,
                user_id: str = Depends(get_user_id),
                group_service: GroupService = Depends(Provide[TaxiContainer.group_service])):
    group_service.leave(user_id, group_id)
