import pytest
from . import setup


def from_json_to_entity(json):
    cls = json['cls']
    params = {}
    for name, value in json.items():
        if name == 'cls':
            continue

        if name == 'members':
            value = [
                from_json_to_entity(member)
                for member in value
            ]

        params[name] = value

    return cls(**params)


def test_participate_success():
    taxi_group = from_json_to_entity(setup.taxi_group_1)

    user_id = 'user3'
    taxi_group.participate(user_id)

    assert user_id in [member.user_id for member in taxi_group.members]
