import pytest
from . import setup
from webapp.common.exceptions import domain
from webapp.domain.taxi_group.entity.status import Status


def test_success_close_to_settle():
    taxi_group = setup.from_json_to_entity(setup.taxi_group_close)

    taxi_group.settle()

    assert taxi_group.status == Status.SETTLE


def test_fail_open_to_settle():
    taxi_group = setup.from_json_to_entity(setup.taxi_group_open)

    with pytest.raises(domain.InvalidState) as e:
        taxi_group.settle()
    assert str(e.value) == "'OPEN' -> 'SETTLE'는 허용되지 않는 상태코드 변경입니다."


def test_fail_complete_to_settle():
    taxi_group = setup.from_json_to_entity(setup.taxi_group_complete)

    with pytest.raises(domain.InvalidState) as e:
        taxi_group.settle()
    assert str(e.value) == "'COMPLETE' -> 'SETTLE'는 허용되지 않는 상태코드 변경입니다."
