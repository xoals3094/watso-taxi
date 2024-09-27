import pytest
from . import setup
from webapp.common.exceptions import domain
from webapp.domain.taxi_group.entity.status import Status


def test_success_settle_to_complete():
    taxi_group = setup.from_json_to_entity(setup.taxi_group_settle)

    taxi_group.complete()

    assert taxi_group.status == Status.COMPLETE


def test_fail_open_to_complete():
    taxi_group = setup.from_json_to_entity(setup.taxi_group_open)

    with pytest.raises(domain.InvalidState) as e:
        taxi_group.complete()
    assert str(e.value) == "'OPEN' -> 'COMPLETE'는 허용되지 않는 상태코드 변경입니다."


def test_fail_close_to_complete():
    taxi_group = setup.from_json_to_entity(setup.taxi_group_close)

    with pytest.raises(domain.InvalidState) as e:
        taxi_group.complete()
    assert str(e.value) == "'CLOSE' -> 'COMPLETE'는 허용되지 않는 상태코드 변경입니다."
