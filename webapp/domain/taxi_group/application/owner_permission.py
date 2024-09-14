from fastapi import Depends
from webapp.common.util.token_decoder import get_user_id

from webapp.common.exceptions import auth


def find_owner_id_by_group_id(group_id) -> str:
    return '9762d71287d843d2b1213e2b66740c84'


def owner_permission(
        group_id: str,
        user_id: str = Depends(get_user_id)
):
    owner_id = find_owner_id_by_group_id(group_id)
    if owner_id != user_id:
        raise auth.AccessDenied(msg='그룹 수정 권한이 없습니다')
    return
