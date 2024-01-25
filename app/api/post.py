from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from datetime import datetime
from dependency_injector.wiring import inject, Provide
from typing import List
from src.post_container import PostContainer

from logic.taxi.post.application.port.incoming.PostWriteUseCase import PostWriteUseCase
from logic.taxi.post.application.port.incoming.PostQueryUseCase import PostQueryUseCase

from.auth import get_user_id

post_router = APIRouter()


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
    id: str
    name: str


class PointsModel(BaseModel):
    depart_point: PointModel
    arrive_point: PointModel


class MemberModel(BaseModel):
    current_member: int
    max_member: int


class ResponsePostsListModel(BaseModel):
    id: str = Field(..., description='게시글 ID', examples=['654601bf3d9ff6479fcdabcd'])
    owner: OwnerModel
    point: PointsModel
    depart_datetime: datetime = Field(..., description='출발 시간', examples=['2023-11-04T08:32:19.505+00:00'])
    fee: int = Field(..., description='비용', examples=['6200'])
    member: MemberModel


class MemberDetailModel(BaseModel):
    current_member: int
    max_member: int
    members: List[str]


class ResponsePostDetailModel(BaseModel):
    id: str = Field(..., description='게시글 ID', examples=['654601bf3d9ff6479fcdabcd'])
    owner: OwnerModel
    point: PointsModel
    depart_datetime: datetime = Field(..., description='출발 시간', examples=['2023-11-04T08:32:19.505+00:00'])
    status: str
    fee: int = Field(..., description='비용', examples=['6200'])
    member: MemberDetailModel


class RequestModifyModel(BaseModel):
    notice: str


class RequestChangeStatusModel(BaseModel):
    status: str


@post_router.get('/', response_model=List[ResponsePostsListModel], tags=['post'])
@inject
async def get_posts(depart_point_id: str,
                    arrive_point_id: str,
                    depart_datetime: datetime,
                    user_id: str = Depends(get_user_id),
                    post_use_case: PostQueryUseCase = Depends(Provide[PostContainer.post_query_service])):

    posts = post_use_case.get_list(user_id, depart_point_id, arrive_point_id, depart_datetime)
    return [post.json for post in posts]


@post_router.post('/', status_code=201, response_model=ResponseCreatePostModel, tags=['post'])
@inject
async def create_post(req: RequestCreatePostModel,
                      user_id: str = Depends(get_user_id),
                      post_use_case: PostWriteUseCase = Depends(Provide[PostContainer.post_write_service])):

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
                          post_use_case: PostQueryUseCase = Depends(Provide[PostContainer.post_query_service])):
    post = post_use_case.get(post_id)
    return post.json


@post_router.patch('/{post_id}', tags=['post'])
@inject
async def patch_post(req: RequestModifyModel,
                     post_id: str,
                     user_id: str = Depends(get_user_id),
                     post_use_case: PostWriteUseCase = Depends(Provide[PostContainer.post_write_service])):
    post_use_case.modify(user_id, post_id, req.notice)


@post_router.patch('/{post_id}/status', tags=['post'])
@inject
async def update_status(req: RequestChangeStatusModel,
                        post_id: str,
                        user_id: str = Depends(get_user_id),
                        post_use_case: PostWriteUseCase = Depends(Provide[PostContainer.post_write_service])):
    post_use_case.change_status(user_id, post_id, req.status)


@post_router.post('/{post_id}/member')
@inject
async def join(post_id: str,
               user_id: str = Depends(get_user_id),
               post_use_case: PostWriteUseCase = Depends(Provide[PostContainer.post_write_service])):
    post_use_case.join(user_id, post_id)


@post_router.delete('/{post_id}/member')
@inject
async def quit(post_id: str,
               user_id: str = Depends(get_user_id),
               post_use_case: PostWriteUseCase = Depends(Provide[PostContainer.post_write_service])):
    post_use_case.quit(user_id, post_id)


# @post_router.delete('/{post_id}', tags=['post'])
# @inject
# async def delete_post(post_id: str,
#                       user_id: str = Depends(get_user_id),
#                       post_use_case: PostWriteUseCase = Depends(Provide[PostContainer.post_write_service])):
#     post_use_case.delete(post_id, user_id)
