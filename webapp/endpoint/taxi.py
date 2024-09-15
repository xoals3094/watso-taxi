from fastapi import APIRouter, Depends, Query, status
from dependency_injector.wiring import inject, Provide
from datetime import datetime

from webapp.common.src.taxi_container import TaxiContainer
from webapp.common.util.token_decoder import get_user_id
from webapp.domain.taxi_group.application.taxi_group_service import TaxiGroupService
from webapp.domain.taxi_group.application.query_service import QueryService
from webapp.domain.taxi_group.application.owner_permission import owner_permission

from .models.taxi import (
    TaxiGroupCreate,
    GroupId,
    TaxiGroup,
    GroupQueryOption,
    Direction,
    FareUpdate,
    FareDetail
)

taxi_router = APIRouter()


@taxi_router.post(
    '',
    status_code=status.HTTP_201_CREATED,
    response_model=GroupId,
)
@inject
async def create_taxi_group(
        req: TaxiGroupCreate,
        user_id=Depends(get_user_id),
        taxi_group_service: TaxiGroupService = Depends(Provide[TaxiContainer.taxi_group_service])
) -> GroupId:

    group_id = taxi_group_service.create(
        owner_id=user_id,
        max_members=req.max_members,
        departure_datetime=req.departure_datetime,
        direction=req.direction
    )

    return GroupId(group_id=group_id)


@taxi_router.get(
    '',
    response_model=list[TaxiGroup]
)
@inject
async def get_taxi_groups(
        option: GroupQueryOption = Query(..., description='조회 옵션'),
        direction: Direction = Query(Direction.CAMPUS, description='조회할 방향'),
        departure_datetime: datetime = Query(datetime.now(), description='조회할 방향'),
        user_id: str = Depends(get_user_id),
        query_service: QueryService = Depends(Provide[TaxiContainer.query_service])
) -> list[TaxiGroup]:

    groups = query_service.get_taxi_group_list(option, direction, user_id, departure_datetime)
    return groups


@taxi_router.get(
    '/history',
    response_model=list[TaxiGroup]
)
@inject
async def get_taxi_group_history(
        user_id: str = Depends(get_user_id),
        query_service: QueryService = Depends(Provide[TaxiContainer.query_service])
) -> list[TaxiGroup]:

    groups = query_service.get_history(user_id)
    return groups


@taxi_router.get(
    '/{group_id}',
    response_model=TaxiGroup
)
@inject
async def get_taxi_group_detail(
        group_id: str,
        user_id: str = Depends(get_user_id),
        query_service: QueryService = Depends(Provide[TaxiContainer.query_service])
) -> TaxiGroup:

    group = query_service.get_taxi_group(group_id=group_id, user_id=user_id)
    return group


@taxi_router.get(
    '/{group_id}/fare',
    response_model=FareDetail
)
@inject
async def get_fare(
        group_id: str,
        query_service: QueryService = Depends(Provide[TaxiContainer.query_service])
) -> FareDetail:

    fare = query_service.get_fare(group_id=group_id)
    return fare


@taxi_router.patch(
    '/{group_id}/fare',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(owner_permission)],
)
@inject
async def update_fare(
        group_id: str,
        req: FareUpdate,
        taxi_group_service: TaxiGroupService = Depends(Provide[TaxiContainer.taxi_group_service])
) -> None:

    members = [(member.id, member.cost) for member in req.members]
    taxi_group_service.update_fare(
        group_id=group_id,
        fare=req.fare,
        members=members
    )


@taxi_router.patch(
    '/{group_id}/open',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(owner_permission)],
)
@inject
async def open(
        group_id: str,
        taxi_group_service: TaxiGroupService = Depends(Provide[TaxiContainer.taxi_group_service])
) -> None:

    taxi_group_service.open(group_id=group_id)


@taxi_router.patch(
    '/{group_id}/close',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(owner_permission)],
)
@inject
async def close(
        group_id: str,
        taxi_group_service: TaxiGroupService = Depends(Provide[TaxiContainer.taxi_group_service])
) -> None:

    taxi_group_service.close(group_id=group_id)


@taxi_router.patch(
    '/{group_id}/settle',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(owner_permission)],
)
@inject
async def settle(
        group_id: str,
        taxi_group_service: TaxiGroupService = Depends(Provide[TaxiContainer.taxi_group_service])
) -> None:

    taxi_group_service.settle(group_id=group_id)


@taxi_router.patch(
    '/{group_id}/complete',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(owner_permission)],
)
@inject
async def complete(
        group_id: str,
        taxi_group_service: TaxiGroupService = Depends(Provide[TaxiContainer.taxi_group_service])
) -> None:

    taxi_group_service.complete(group_id=group_id)


@taxi_router.post(
    '/{group_id}/members',
    status_code=status.HTTP_204_NO_CONTENT,
)
@inject
async def participate(
        group_id: str,
        user_id: str = Depends(get_user_id),
        taxi_group_service: TaxiGroupService = Depends(Provide[TaxiContainer.taxi_group_service])
) -> None:

    taxi_group_service.participate(group_id=group_id, user_id=user_id)


@taxi_router.delete(
    '/{group_id}/members',
    status_code=status.HTTP_204_NO_CONTENT,
)
@inject
async def leave(
        group_id: str,
        user_id: str = Depends(get_user_id),
        taxi_group_service: TaxiGroupService = Depends(Provide[TaxiContainer.taxi_group_service])
) -> None:

    taxi_group_service.leave(group_id=group_id, user_id=user_id)
