from datetime import datetime, timedelta

participate_success = {
    'id': 'test1',
    'owner_id': 'owner_id',
    'is_open': True,
    'max_members': 4,
    'fare': 6000,
    'status': 'OPEN',
    'departure_datetime': datetime.now() + timedelta(minutes=30),
    'direction': 'STATION',
    'members': [
        {
            'group_id': 'test1',
            'user_id': 'test-user1',
            'cost': 3000
        },
        {
            'group_id': 'test1',
            'user_id': 'test-user2',
            'cost': 3000
        }
    ]
}
