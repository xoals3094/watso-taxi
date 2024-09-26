from datetime import datetime, timedelta
from webapp.domain.taxi_group.entity.taxi_group import TaxiGroup, TaxiGroupMember


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


taxi_group_1 = {
    'cls': TaxiGroup,
    'id': 'test1',
    'owner_id': 'test-user1',
    'is_open': True,
    'max_members': 4,
    'fare': 6000,
    'status': 'OPEN',
    'departure_datetime': datetime.now() + timedelta(minutes=30),
    'direction': 'STATION',
    'members': [
        {
            'cls': TaxiGroupMember,
            'group_id': 'test1',
            'user_id': 'test-user1',
            'cost': 3000
        },
        {
            'cls': TaxiGroupMember,
            'group_id': 'test1',
            'user_id': 'test-user2',
            'cost': 3000
        }
    ]
}


taxi_group_2 = {
    'cls': TaxiGroup,
    'id': 'test1',
    'owner_id': 'test-user1',
    'is_open': False,
    'max_members': 4,
    'fare': 6000,
    'status': 'CLOSE',
    'departure_datetime': datetime.now() + timedelta(minutes=30),
    'direction': 'STATION',
    'members': [
        {
            'cls': TaxiGroupMember,
            'group_id': 'test1',
            'user_id': 'test-user1',
            'cost': 3000
        },
        {
            'cls': TaxiGroupMember,
            'group_id': 'test1',
            'user_id': 'test-user2',
            'cost': 3000
        }
    ]
}


taxi_group_3 = {
    'cls': TaxiGroup,
    'id': 'test1',
    'owner_id': 'test-user1',
    'is_open': True,
    'max_members': 2,
    'fare': 6000,
    'status': 'OPEN',
    'departure_datetime': datetime.now() + timedelta(minutes=30),
    'direction': 'STATION',
    'members': [
        {
            'cls': TaxiGroupMember,
            'group_id': 'test1',
            'user_id': 'test-user1',
            'cost': 3000
        },
        {
            'cls': TaxiGroupMember,
            'group_id': 'test1',
            'user_id': 'test-user2',
            'cost': 3000
        }
    ]
}