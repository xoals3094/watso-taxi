from logic.taxi.post.domain.Post import Post
from logic.taxi.post.application.port.outgoing.PostUpdateDao import PostUpdateDao
from bson import ObjectId


class MongoDBPostUpdateDao(PostUpdateDao):
    def __init__(self, mongodb_connection):
        self.db = mongodb_connection['taxi']

    def update_status(self, post: Post):
        find = {'_id': ObjectId(post.id)}
        update = {'$set': {'status': post.status}}
        self.db.post.update_one(find, update)

    def update_content(self, post: Post):
        find = {'_id': ObjectId(post.id)}
        update = {
            '$set': {
                'depart_time': post.depart_time,
                'max_member': post.max_member,
                'content': post.content
            }
        }
        self.db.post.update_one(find, update)

    def update_users(self, post: Post):
        find = {'_id': ObjectId(post._id)}
        update = {'$set': {'users': post.users}}

        self.db.post.update_one(find, update)
