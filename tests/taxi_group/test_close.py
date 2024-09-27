import pytest
from . import setup
from webapp.common.exceptions import domain
from webapp.domain.taxi_group.entity.status import Status


def test_success_open_to_close():
    taxi_group = setup.from_json_to_entity(setup.taxi_group_open)

    taxi_group.close()

    assert taxi_group.status == Status.CLOSE


def test_fail_settle_to_close():
    taxi_group = setup.from_json_to_entity(setup.taxi_group_settle)

    with pytest.raises(domain.InvalidState) as e:
        taxi_group.close()
    assert str(e.value) == "'SETTLE' -> 'CLOSE'는 허용되지 않는 상태코드 변경입니다."


def test_fail_complete_to_close():
    taxi_group = setup.from_json_to_entity(setup.taxi_group_complete)

    with pytest.raises(domain.InvalidState) as e:
        taxi_group.close()
    assert str(e.value) == "'COMPLETE' -> 'CLOSE'는 허용되지 않는 상태코드 변경입니다."
    