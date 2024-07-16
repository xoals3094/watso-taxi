from fastapi import Depends
from util.token_decoder import get_user_id
from dependency_injector.wiring import inject, Provide

from src.taxi_container import TaxiContainer

from .dao import MySQLOwnerDao
from exceptions import auth


@inject
def owner_permission(group_id: int,
                     user_id: int = Depends(get_user_id),
                     owner_dao: MySQLOwnerDao = Depends(Provide[TaxiContainer.owner_dao])):
    owner_id = owner_dao.find_owner_id_by_group_id(group_id)
    if owner_id != user_id:
        raise auth.AccessDenied(msg='그룹 수정 권한이 없습니다')
    return
