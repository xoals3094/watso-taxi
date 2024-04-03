# review
from exceptions import PersistenceException
from bson import ObjectId
from domain.taxi.group.util.mapper import GroupEntityMapper
from domain.taxi.group.entity.group import Group
from domain.taxi.group.application.group_service import GroupRepository


class MongoDBGroupRepository(GroupRepository):
    def __init__(self, mongodb_connection):
        self.db = mongodb_connection['watso']

    def find_group_by_id(self, group_id: str) -> Group:
        find = {'_id': ObjectId(group_id)}
        group_json = self.db.group.find_one(find)
        if group_json is None:
            raise PersistenceException.ResourceNotFoundException(
                msg=f'그룹 정보를 찾을 수 없습니다. id={group_id}'
            )

        return GroupEntityMapper.mapping_group_entity(group_json)

    def save(self, group: Group):
        find = {'_id': ObjectId(group.owner_id)}
        member = self.db.member.find_one(find)
        if member is None:
            raise PersistenceException.ResourceNotFoundException(
                msg=f'유저 정보를 찾을 수 없습니다 id={group.owner_id}'
            )

        find = {'_id': ObjectId(group.point.depart_point_id)}
        depart_point = self.db.group.find_one(find)
        if depart_point is None:
            raise PersistenceException.ResourceNotFoundException(
                msg=f'포인트 정보를 찾을 수 없습니다 id={group.point.depart_point_id}'
            )

        find = {'_id': ObjectId(group.point.arrive_point_id)}
        arrive_point = self.db.point.find_one(find)
        if arrive_point is None:
            raise PersistenceException.ResourceNotFoundException(
                msg=f'포인트 정보를 찾을 수 없습니다 id={group.point.arrive_point_id}'
            )

        data = {
            '_id': ObjectId(group.id),
            'owner': {
                '_id': member['_id'],
                'nickname': member['nickname']
            },
            'point': {
                'depart_point': {
                    '_id': depart_point['_id'],
                    'name': depart_point['name']
                },
                'arrive_point': {
                    '_id': arrive_point['_id'],
                    'name': arrive_point['name']
                }
            },
            'depart_datetime': group.depart_datetime,
            'status': group.status,
            'fee': group.fee,
            'member': {
                'max_member': group.member.max_member,
                'members': [ObjectId(member) for member in group.member.members]
            },
            'notice': group.notice,
        }
        self.db.group.insert_one(data)

    def delete(self, group_id: str):
        find = {'_id': ObjectId(group_id)}
        update = {'$set': {'status': 'canceled'}}
        self.db.group.update_one(find, update)
