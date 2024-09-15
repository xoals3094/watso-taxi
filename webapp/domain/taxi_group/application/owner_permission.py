from fastapi import Depends
from sqlalchemy import select
from webapp.common.database import get_session
from webapp.common.util.token_decoder import get_user_id
from webapp.domain.taxi_group.entity.taxi_group import TaxiGroup

from webapp.common.exceptions import auth


def find_owner_id_by_group_id(group_id: str, session=Depends(get_session)) -> str:
    stmt = select(TaxiGroup.owner_id).where(
        TaxiGroup.id == group_id
    )

    result = session.execute(stmt)
    owner_id = result.scalar_one()
    return owner_id


def owner_permission(
        owner_id: str = Depends(find_owner_id_by_group_id),
        user_id: str = Depends(get_user_id)
):
    if owner_id != user_id:
        raise auth.AccessDenied(msg='그룹 수정 권한이 없습니다')
    return
