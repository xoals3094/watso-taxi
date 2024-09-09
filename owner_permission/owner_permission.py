from fastapi import Depends
from webapp.common.util.token_decoder import get_user_id

from webapp.common.src.taxi_container import TaxiContainer

from .dao import MySQLOwnerDao
from webapp.common.exceptions import auth


def owner_permission(group_id: int,
                     user_id: int = Depends(get_user_id),
                     owner_dao: MySQLOwnerDao = Depends(TaxiContainer.owner_dao)):
    owner_id = owner_dao.find_owner_id_by_group_id(group_id)
    if owner_id != user_id:
        raise auth.AccessDenied(msg='그룹 수정 권한이 없습니다')
    return
