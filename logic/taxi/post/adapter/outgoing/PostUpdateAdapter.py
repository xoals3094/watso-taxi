from logic.taxi.post.domain.Post import Post
from logic.taxi.post.application.port.outgoing.PostUpdateDao import PostUpdateDao
from bson import ObjectId


class MongoDBPostUpdateDao(PostUpdateDao):
    def __init__(self, mongodb_connection):
        self.db = mongodb_connection['watso']

    def update(self, post: Post):
        find = {'_id': ObjectId(post.id)}
        update = {'$set': {'notice': post.notice}}
        self.db.post.update_one(find, update)

    def update_status(self, post: Post):
        find = {'_id': ObjectId(post.id)}
        update = {'$set': {'status': post.status}}
        self.db.post.update_one(find, update)

    def update_members(self, post: Post):
        find = {'_id': ObjectId(post.id)}
        update = {'$set': {'member.members': [ObjectId(member) for member in post.member.members]}}
        self.db.post.update_one(find, update)
