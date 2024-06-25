from .taxi_group_api import taxi_group_router
from fastapi import Depends, status
from pydantic import BaseModel, Field
from datetime import datetime
from dependency_injector.wiring import inject, Provide

from domain.group.application.group_service import GroupService
from domain.taxi_group.application.taxi_group_service import TaxiGroupService
from src.taxi_container import TaxiContainer

from app.util.token_decoder import get_user_id


class RequestCreateGroupModel(BaseModel):
    depart_point_id: str = Field(..., description='출발 지점 ID', examples=['ObjectId'])
    arrive_point_id: str = Field(..., description='도착 지점 ID', examples=['ObjectId'])
    depart_datetime: datetime = Field(..., description='출발 시간', examples=[datetime.now()])
    max_member: int = Field(..., description='최대 인원', examples=[3])
    notice: str = Field(..., description='공지사항', examples=['기숙사에서 내리지만 장소 협의 가능합니다'])


class ResponseCreateGroupModel(BaseModel):
    post_id: str = Field(..., description='생성된 게시글 ID', examples=['ObjectId'])


@taxi_group_router.post('/{group_id}/open', status_code=status.HTTP_204_NO_CONTENT, tags=['taxi-group-command'])
@inject
async def open_group(group_id: str,
                     user_id: str = Depends(get_user_id),
                     group_service: GroupService = Depends(Provide[TaxiContainer.taxi_group_service])):
    group_service.owner_permission(user_id, group_id)
    group_service.open(group_id)


@taxi_group_router.post('/{group_id}/close', status_code=status.HTTP_204_NO_CONTENT, tags=['taxi-group-command'])
@inject
async def close_group(group_id: str, user_id: str = Depends(get_user_id),
                      group_service: GroupService = Depends(Provide[TaxiContainer.taxi_group_service])):
    group_service.owner_permission(user_id, group_id)
    group_service.close(group_id)


@taxi_group_router.post('/{group_id}/member', status_code=204, tags=['taxi-group-command'])
@inject
async def participate(group_id: str, user_id: str = Depends(get_user_id),
                      group_service: GroupService = Depends(Provide[TaxiContainer.taxi_group_service])):
    group_service.participate(user_id, group_id)


@taxi_group_router.delete('/{group_id}/member', status_code=204, tags=['taxi-group-command'])
@inject
async def leave(group_id: str, user_id: str = Depends(get_user_id),
                group_service: GroupService = Depends(Provide[TaxiContainer.taxi_group_service])):
    group_service.leave(user_id, group_id)


@taxi_group_router.post('', status_code=201, response_model=ResponseCreateGroupModel, tags=['taxi-group-command'])
@inject
async def create_taxi_group(req: RequestCreateGroupModel, user_id: int = Depends(get_user_id),
                            taxi_group_service: TaxiGroupService = Depends(Provide[TaxiContainer.taxi_group_service])):
    group_id = taxi_group_service.create(owner_id=user_id,
                                         max_member=req.max_member,
                                         depart_datetime=req.depart_datetime,
                                         depart_location_id=req.depart_location_id,
                                         arrive_location_id=req.arrive_location_id)

    return {'group_id': group_id}


@taxi_group_router.post('/{group_id}/settle', status_code=status.HTTP_204_NO_CONTENT, tags=['taxi-group-command'])
@inject
async def settle(group_id: str, user_id: str = Depends(get_user_id),
                 taxi_group_service: TaxiGroupService = Depends(Provide[TaxiContainer.taxi_group_service])):
    taxi_group_service.owner_permission(user_id, group_id)
    taxi_group_service.settle(group_id)


@taxi_group_router.post('/{group_id}/complete', status_code=status.HTTP_204_NO_CONTENT, tags=['taxi-group-command'])
@inject
async def complete(group_id: str, user_id: str = Depends(get_user_id),
                   taxi_group_service: TaxiGroupService = Depends(Provide[TaxiContainer.taxi_group_service])):
    taxi_group_service.owner_permission(user_id, group_id)
    taxi_group_service.complete(group_id)



