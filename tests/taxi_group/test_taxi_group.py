import pytest
from . import setup
from webapp.domain.taxi_group.entity.taxi_group import TaxiGroup, TaxiGroupMember


def from_json_to_entity(cls, json):
    params = {}
    for name, value in json.items():
        if name == 'members':
            value = [
                from_json_to_entity(TaxiGroupMember, member)
                for member in value
            ]

        params[name] = value

    return cls(**params)


def test_participate_success():
    taxi_group = from_json_to_entity(TaxiGroup, setup.participate_success)

    user_id = 'user3'
    taxi_group.participate(user_id)

    assert user_id in [member.user_id for member in taxi_group.members]
