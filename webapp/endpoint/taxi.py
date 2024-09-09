from fastapi import APIRouter, Depends, Query, status
from dependency_injector.wiring import inject, Provide
from datetime import datetime

from webapp.domain.taxi.application.taxi_group_service import TaxiGroupService
from webapp.domain.taxi.application.query_service import QueryService

from webapp.common.src.taxi_container import TaxiContainer
from webapp.common.util.token_decoder import get_user_id

from .models.taxi import (
    TaxiGroupCreate,
    GroupId,
    FeeUpdate,
    TaxiGroup,
    GroupQueryOption,
    Direction,
    BillsDetail
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
        max_member=req.max_member,
        depart_datetime=req.depart_datetime,
        direction=req.direction
    )

    return GroupId(group_id=group_id)


@taxi_router.get(
    '',
    response_model=list[TaxiGroup]
)
@inject
async def get_taxi_groups(
        option: GroupQueryOption = Query(None, description='조회 옵션'),
        direction: Direction = Query(None, description='조회할 방향'),
        departure_datetime: datetime = Query(datetime.now(), description='조회할 방향'),
        user_id: int = Depends(get_user_id),
        query_service: QueryService = Depends(TaxiContainer.query_service)
):
    query_service.get_taxi_group_list(option, direction, user_id, departure_datetime)

    return [group.json for group in groups]


@taxi_router.get(
    '/{group_id}',
    response_model=TaxiGroup
)
@inject
async def get_taxi_group_detail(
        group_id: int,
        user_id: int = Depends(get_user_id),
        query_service: QueryService = Depends(TaxiContainer.query_service)
):
    group = group_query.find_group(user_id, group_id)
    return group.get_json_detail(user_id)


@taxi_router.get(
    '/{group_id}/fee',
    response_model=BillsDetail
)
@inject
async def get_bills(
        group_id: int,
        query_service: QueryService = Depends(TaxiContainer.query_service)
):
    group = group_query.find_bills_by_group_id(group_id)
    return group.json


@taxi_router.patch(
    '/{group_id}/fee',
    status_code=status.HTTP_204_NO_CONTENT,
    # dependencies=[Depends(owner_permission)],
)
@inject
async def update_fee(
        group_id: int,
        req: FeeUpdate,
        taxi_group_service: TaxiGroupService = Depends(Provide[TaxiContainer.taxi_group_service])
):
    taxi_group_service.set_fee(group_id=group_id, fee=req.fee, bills=req.bills)


@taxi_router.patch(
    '/{group_id}/open',
    status_code=status.HTTP_204_NO_CONTENT,
    # dependencies=[Depends(owner_permission)],
)
@inject
async def recruit(
        group_id: int,
        taxi_group_service: TaxiGroupService = Depends(Provide[TaxiContainer.taxi_group_service])
):
    taxi_group_service.open(group_id=group_id)


@taxi_router.patch(
    '/{group_id}/close',
    status_code=status.HTTP_204_NO_CONTENT,
    # dependencies=[Depends(owner_permission)],
)
@inject
async def close(
        group_id: int,
        taxi_group_service: TaxiGroupService = Depends(Provide[TaxiContainer.taxi_group_service])
):
    taxi_group_service.close(group_id=group_id)


@taxi_router.patch(
    '/{group_id}/settle',
    status_code=status.HTTP_204_NO_CONTENT,
    # dependencies=[Depends(owner_permission)],
)
@inject
async def settle(
        group_id: int,
        taxi_group_service: TaxiGroupService = Depends(Provide[TaxiContainer.taxi_group_service])
):
    taxi_group_service.settle(group_id=group_id)


@taxi_router.patch(
    '/{group_id}/complete',
    status_code=status.HTTP_204_NO_CONTENT,
    # dependencies=[Depends(owner_permission)],
)
@inject
async def complete(
        group_id: int,
        taxi_group_service: TaxiGroupService = Depends(Provide[TaxiContainer.taxi_group_service])
):
    taxi_group_service.complete(group_id=group_id)


@taxi_router.post(
    '/{group_id}/member',
    status_code=status.HTTP_204_NO_CONTENT,
)
@inject
async def participate(
        group_id: int,
        user_id: int = Depends(get_user_id),
        taxi_group_service: TaxiGroupService = Depends(Provide[TaxiContainer.taxi_group_service])
):
    taxi_group_service.participate(group_id, user_id)


@taxi_router.delete(
    '/{group_id}/member',
    status_code=status.HTTP_204_NO_CONTENT,
)
@inject
async def leave(
        group_id: int,
        user_id: int = Depends(get_user_id),
        taxi_group_service: TaxiGroupService = Depends(Provide[TaxiContainer.taxi_group_service])
):
    taxi_group_service.leave(group_id, user_id)











# @query_router.get('/{group_id}/settle-code', response_model=ResponseURL, tags=['taxi-query'])
# async def get_settlement_code(group_id: int,
#                               user_id: int = Depends(get_user_id),
#                               payment_service: PaymentService = PaymentContainer.payment_service):
#     url = payment_service.create_url(group_id, user_id)
#     return {
#         'url': url
#     }