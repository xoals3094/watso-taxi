import pytest
from . import setup
from webapp.common.exceptions import domain


def test_success():
    taxi_group = setup.from_json_to_entity(setup.taxi_group_open)

    user_id = 'test-user2'
    taxi_group.leave(user_id)

    assert user_id not in [member.user_id for member in taxi_group.members]


def test_fail_owner_member():
    taxi_group = setup.from_json_to_entity(setup.taxi_group_open)
    user_id = taxi_group.owner_id

    with pytest.raises(domain.LeaveFailed) as e:
        taxi_group.leave(user_id)
    assert str(e.value) == '그룹장 유저는 탈퇴가 불가능합니다'


def test_fail_not_open():
    taxi_group = setup.from_json_to_entity(setup.taxi_group_close)
    user_id = 'test-user2'

    with pytest.raises(domain.LeaveFailed) as e:
        taxi_group.leave(user_id)
    assert str(e.value) == '탈퇴가 불가능한 그룹입니다 is_open=False'


def test_fail_not_exist_member():
    taxi_group = setup.from_json_to_entity(setup.taxi_group_open)
    user_id = 'test-user3'

    with pytest.raises(domain.LeaveFailed) as e:
        taxi_group.leave(user_id)
    assert str(e.value) == '참여하지 않은 유저입니다'
