from exceptions import PersistenceException
from bson import ObjectId
from logic.taxi.post.adapter.outgoing.PostMapper import PostMapper
from logic.taxi.post.domain.Post import Post
from logic.taxi.post.application.port.outgoing.PostRepository import PostRepository


class MongoDBPostRepository(PostRepository):
    def __init__(self, mongodb_connection):
        self.db = mongodb_connection['watso']

    def find_post_by_id(self, post_id: str) -> Post:
        find = {'_id': ObjectId(post_id)}
        post_json = self.db.post.find_one(find)
        if post_json is None:
            raise PersistenceException.ResourceNotFoundException(
                msg=f'게시글 정보를 찾을 수 없습니다. id={post_id}'
            )

        return PostMapper.post_mapping(post_json)

    def save(self, post: Post):
        find = {'_id': ObjectId(post.owner_id)}
        user = self.db.user.find_one(find)
        if user is None:
            raise PersistenceException.ResourceNotFoundException(
                msg=f'유저 정보를 찾을 수 없습니다 id={post.owner_id}'
            )

        find = {'_id': ObjectId(post.point.depart_point_id)}
        depart_point = self.db.point.find_one(find)
        if depart_point is None:
            raise PersistenceException.ResourceNotFoundException(
                msg=f'포인트 정보를 찾을 수 없습니다 id={post.point.depart_point_id}'
            )

        find = {'_id': ObjectId(post.point.arrive_point_id)}
        arrive_point = self.db.point.find_one(find)
        if arrive_point is None:
            raise PersistenceException.ResourceNotFoundException(
                msg=f'포인트 정보를 찾을 수 없습니다 id={post.point.arrive_point_id}'
            )

        data = {
            '_id': ObjectId(post.id),
            'owner': {
                '_id': user['_id'],
                'nickname': user['nickname']
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
            'depart_datetime': post.depart_datetime,
            'status': post.status,
            'fee': post.fee,
            'member': {
                'max_member': post.member.max_member,
                'members': [ObjectId(member) for member in post.member.members]
            },
            'notice': post.notice,
        }
        self.db.post.insert_one(data)

    def delete(self, post_id: str):
        find = {'_id': ObjectId(post_id)}
        update = {'$set': {'status': 'canceled'}}
        self.db.post.update_one(find, update)
