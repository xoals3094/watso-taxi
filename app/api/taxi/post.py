from fastapi import APIRouter, Depends, status, Response
from pydantic import BaseModel, Field
from datetime import datetime
from dependency_injector.wiring import inject, Provide
from typing import List

from logic.taxi.post.application.port.incoming.PostWriteUseCase import PostWriteUseCase
from logic.taxi.post.application.port.incoming.PostQueryUseCase import PostQueryUseCase
from src.taxi_container import TaxiContainer

from app.util.token_decoder import get_user_id

post_router = APIRouter(prefix='/post')


class RequestCreatePostModel(BaseModel):
    depart_point_id: str = Field(..., description='출발 지점 ID', examples=['ObjectId'])
    arrive_point_id: str = Field(..., description='도착 지점 ID', examples=['ObjectId'])
    depart_datetime: datetime = Field(..., description='출발 시간', examples=[datetime.now()])
    max_member: int = Field(..., description='최대 인원', examples=[3])
    notice: str = Field(..., description='공지사항', examples=['기숙사에서 내리지만 장소 협의 가능합니다'])


class ResponseCreatePostModel(BaseModel):
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


class ResponsePostsListModel(BaseModel):
    id: str = Field(..., description='게시글 ID', examples=['654601bf3d9ff6479fcdabcd'])
    owner: OwnerModel
    point: PointsModel
    depart_datetime: datetime = Field(..., description='출발 시간', examples=[datetime.now()])
    fee: int = Field(..., description='비용', examples=['6200'])
    member: MemberModel


class MemberDetailModel(BaseModel):
    current_member: int = Field(..., description='현재 인원', examples=[3])
    max_member: int = Field(..., description='최대 인원', examples=[4])
    members: List[str] = Field(..., description='참여자 ID 목록', examples=[['ObjectId']])


class ResponsePostDetailModel(BaseModel):
    id: str = Field(..., description='게시글 ID', examples=['654601bf3d9ff6479fcdabcd'])
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


@post_router.get('', response_model=List[ResponsePostsListModel], tags=['post'])
@inject
async def get_posts(depart_point_id: str,
                    arrive_point_id: str,
                    depart_datetime: datetime,
                    user_id: str = Depends(get_user_id),
                    post_use_case: PostQueryUseCase = Depends(Provide[TaxiContainer.post_query_service])):

    posts = post_use_case.get_list(user_id, depart_point_id, arrive_point_id, depart_datetime)
    return [post.json for post in posts]


@post_router.post('', status_code=201, response_model=ResponseCreatePostModel, tags=['post'])
@inject
async def create_post(req: RequestCreatePostModel,
                      user_id: str = Depends(get_user_id),
                      post_use_case: PostWriteUseCase = Depends(Provide[TaxiContainer.post_write_service])):

    post_id = post_use_case.create(owner_id=user_id,
                                   depart_point_id=req.depart_point_id,
                                   arrive_point_id=req.arrive_point_id,
                                   depart_datetime=req.depart_datetime,
                                   max_member=req.max_member,
                                   notice=req.notice)
    return {'post_id': post_id}


@post_router.get('/{post_id}', response_model=ResponsePostDetailModel, tags=['post'])
@inject
async def get_post_detail(post_id: str,
                          post_use_case: PostQueryUseCase = Depends(Provide[TaxiContainer.post_query_service])):
    post = post_use_case.get(post_id)
    return post.json


@post_router.patch('/{post_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['post'])
@inject
async def patch_post(req: RequestModifyModel,
                     post_id: str,
                     user_id: str = Depends(get_user_id),
                     post_use_case: PostWriteUseCase = Depends(Provide[TaxiContainer.post_write_service])):
    post_use_case.modify(user_id, post_id, req.notice)


@post_router.patch('/{post_id}/status', status_code=204, tags=['post'])
@inject
async def update_status(req: RequestChangeStatusModel,
                        post_id: str,
                        user_id: str = Depends(get_user_id),
                        post_use_case: PostWriteUseCase = Depends(Provide[TaxiContainer.post_write_service])):
    post_use_case.change_status(user_id, post_id, req.status)


@post_router.post('/{post_id}/member', status_code=204, tags=['post'])
@inject
async def participate(post_id: str,
                      user_id: str = Depends(get_user_id),
                      post_use_case: PostWriteUseCase = Depends(Provide[TaxiContainer.post_write_service])):
    post_use_case.participate(user_id, post_id)


@post_router.delete('/{post_id}/member', status_code=204, tags=['post'])
@inject
async def leave(post_id: str,
                user_id: str = Depends(get_user_id),
                post_use_case: PostWriteUseCase = Depends(Provide[TaxiContainer.post_write_service])):
    post_use_case.leave(user_id, post_id)
