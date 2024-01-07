from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime
from dependency_injector.wiring import inject, Provide
from typing import List
from src.post_container import PostContainer

from .auth import get_user_id

from logic.taxi.post.application.port.incoming.PostWriteUseCase import PostWriteUseCase
from logic.taxi.post.application.port.incoming.PostQueryUseCase import PostQueryUseCase
from logic.taxi.post.dto.presentation import PostWriteModel

post_router = APIRouter()


class RequestCreatePostModel(BaseModel):
    direction: str = Field(..., description='방향', examples=['station'])
    depart_time: datetime = Field(..., description='출발 시간', examples=[datetime.now()])
    max_member: int = Field(..., description='최대 인원', examples=[3])
    content: str = Field(..., description='상세 내용', examples=['기숙사에서 내리지만 장소 협의 가능합니다'])


class ResponseCreatePostModel(BaseModel):
    post_id: str = Field(..., description='생성된 게시글 ID', examples=['654601bf3d9ff6479fcdabcd'])


class Option(str, Enum):
    all = 'all'
    joinable = 'joinable'
    joined = 'joined'


class RequestGetPostsModel(BaseModel):
    option: Option


class UserModel(BaseModel):
    id: str = Field(..., description='유저 ID', examples=['6545e68874451c47d45bce74'])
    nickname: str = Field(..., description='닉네임', examples=['찰봉'])


class ResponsePostsListModel(BaseModel):
    id: str = Field(..., description='게시글 ID', examples=['654601bf3d9ff6479fcdabcd'])
    user: UserModel
    status: str = Field(..., description='상태 코드', examples=['RECRUITING', 'CLOSE', 'BOARDING', 'SETTLE', 'COMPLETION'])
    direction: str = Field(..., description='방향', examples=['station', 'campus'])
    depart_time: datetime = Field(..., description='출발 시간', examples=['2023-11-04T08:32:19.505+00:00'])
    max_member: int = Field(..., description='최대 인원', examples=['3'])
    users: List[str] = Field(..., description='참여 유저', examples=['6545e68874451c47d45bce74'])


class ResponsePostDetailModel(BaseModel):
    id: str = Field(..., description='게시글 ID', examples=['654601bf3d9ff6479fcdabcd'])
    user: UserModel
    status: str = Field(..., description='상태 코드', examples=['RECRUITING', 'CLOSE', 'BOARDING', 'SETTLE', 'COMPLETION'])
    direction: str = Field(..., description='방향', examples=['station', 'campus'])
    depart_time: datetime = Field(..., description='출발 시간', examples=[datetime.now()])
    max_member: int = Field(..., description='최대 인원', examples=[3])
    content: str = Field(..., description='상세 내용', examples=['기숙사에서 내리지만 장소 협의 가능합니다'])
    users: List[str] = Field(..., description='참여 유저', examples=[['6545e68874451c47d45bce74']])


class RequestModifyModel(BaseModel):
    depart_time: datetime | None = Field(None, description='출발 시간', examples=[datetime.now()])
    max_member: int | None = Field(None, description='최대 인원', examples=[3])
    content: str | None = Field(None, description='상세 내용', examples=['기숙사에서 내리지만 장소 협의 가능합니다'])


@post_router.get('/', response_model=List[ResponsePostsListModel])
@inject
async def get_posts(option: Option,
                    user_id: str = Depends(get_user_id),
                    post_use_case: PostQueryUseCase = Depends(Provide[PostContainer.post_query_service])):

    posts = post_use_case.get_list(option, user_id)
    return [post.json for post in posts]


@post_router.post('/', status_code=201, response_model=ResponseCreatePostModel)
@inject
async def create_post(req: RequestCreatePostModel,
                      user_id: str = Depends(get_user_id),
                      post_use_case: PostWriteUseCase = Depends(Provide[PostContainer.post_write_service])):
    post_write_model = PostWriteModel(direction=req.direction,
                                      depart_time=req.depart_time,
                                      max_member=req.max_member,
                                      content=req.content)
    post_id = post_use_case.create(user_id, post_write_model)
    return {'post_id': post_id}


@post_router.get('/{post_id}', response_model=ResponsePostDetailModel)
@inject
async def get_post_detail(post_id: str,
                          post_use_case: PostQueryUseCase = Depends(Provide[PostContainer.post_query_service])):
    post = post_use_case.get(post_id)
    return post.json


@post_router.patch('/{post_id}')
@inject
async def patch_post(req: RequestModifyModel,
                     post_id: str,
                     user_id: str = Depends(get_user_id),
                     post_use_case: PostWriteUseCase = Depends(Provide[PostContainer.post_write_service])):
    patch_data = req.model_dump(exclude_unset=True)
    post_use_case.modify(user_id, post_id, patch_data)


@post_router.delete('/{post_id}')
@inject
async def delete_post(post_id: str,
                      user_id: str = Depends(get_user_id),
                      post_use_case: PostWriteUseCase = Depends(Provide[PostContainer.post_write_service])):
    post_use_case.delete(post_id, user_id)


# @post_router.patch('/{post_id}/status')
# @inject
# async def patch_status(post_id: str,
#                        user_id: str = Depends(get_user_id),
#                        post_use_case: PostWriteUseCase = Provide[PostContainer.post_update_service]):
#     post_use_case.change_status(g.id, post_id, data['status'])
