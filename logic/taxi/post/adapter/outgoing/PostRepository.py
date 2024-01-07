import exceptions
from bson import ObjectId
from logic.taxi.post.adapter.outgoing.PostMapper import PostMapper
from logic.taxi.post.domain.Post import Post
from logic.taxi.post.application.port.outgoing.PostRepository import PostRepository


class MongoDBPostRepository(PostRepository):
    def __init__(self, mongodb_connection):
        self.db = mongodb_connection['taxi']
        self.user_db = mongodb_connection['auth']

    def find_post_by_id(self, post_id: str) -> Post:
        find = {'_id': ObjectId(post_id)}
        post_json = self.db.post.find_one(find)
        if post_json is None:
            raise exceptions.NotExistPost

        return PostMapper.post_mapping(post_json)

    def save(self, post: Post):
        find = {'_id': ObjectId(post.user_id)}
        user = self.user_db.user.find_one(find)
        nickname = user['nickname']

        data = {
            '_id': ObjectId(post.id),
            'user': {
                '_id': ObjectId(post.user_id),
                'nickname': nickname
            },
            'status': post.status,
            'direction': post.direction,
            'depart_time': post.depart_time,
            'max_member': post.max_member,
            'content': post.content,
            'users': [ObjectId(user_id) for user_id in post.users]
        }
        self.db.post.insert_one(data)

    def delete(self, post_id: str):
        find = {'_id': ObjectId(post_id)}
        update = {'$set': {'status': 'canceled'}}
        self.db.post.update_one(find, update)
