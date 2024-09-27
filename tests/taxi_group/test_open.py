import pytest
from . import setup
from webapp.common.exceptions import domain
from webapp.domain.taxi_group.entity.status import Status


def test_success_close_to_open():
    taxi_group = setup.from_json_to_entity(setup.taxi_group_close)

    taxi_group.open()

    assert taxi_group.status == Status.OPEN


def test_fail_settle_to_open():
    taxi_group = setup.from_json_to_entity(setup.taxi_group_settle)

    with pytest.raises(domain.InvalidState) as e:
        taxi_group.open()
    assert str(e.value) == "'SETTLE' -> 'OPEN'는 허용되지 않는 상태코드 변경입니다."
