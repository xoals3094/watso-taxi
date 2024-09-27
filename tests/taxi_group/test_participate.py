import pytest
from . import setup
from webapp.common.exceptions import domain


def test_success():
    taxi_group = setup.from_json_to_entity(setup.taxi_group_open)

    user_id = 'test-user3'
    taxi_group.participate(user_id)

    assert user_id in [member.user_id for member in taxi_group.members]


def test_fail_owner_member():
    taxi_group = setup.from_json_to_entity(setup.taxi_group_open)
    user_id = taxi_group.owner_id

    with pytest.raises(domain.ParticipationFailed) as e:
        taxi_group.participate(user_id)
    assert str(e.value) == '그룹장 유저는 참여가 불가능합니다'


def test_fail_not_open():
    taxi_group = setup.from_json_to_entity(setup.taxi_group_close)
    user_id = 'test-user3'

    with pytest.raises(domain.ParticipationFailed) as e:
        taxi_group.participate(user_id)
    assert str(e.value) == '참여가 마감된 그룹입니다 is_open=False'


def test_fail_max_members():
    taxi_group = setup.from_json_to_entity(setup.taxi_group_max_members)
    user_id = 'test-user3'

    with pytest.raises(domain.ParticipationFailed) as e:
        taxi_group.participate(user_id)
    assert str(e.value) == '최대 인원에 도달하여 참여 불가능합니다 2/2'


def test_fail_duplicate_member():
    taxi_group = setup.from_json_to_entity(setup.taxi_group_open)
    user_id = taxi_group.members[1].user_id

    with pytest.raises(domain.ParticipationFailed) as e:
        taxi_group.participate(user_id)
    assert str(e.value) == '이미 참여한 유저입니다'
