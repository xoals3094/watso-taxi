from logic.common.push_message.application.port.outgoing.UserIdFinder import UserIdFinder
from bson import ObjectId


class MongoDBUserIdFinder(UserIdFinder):
    def __init__(self, mongodb_connection):
        self.db = mongodb_connection['delivery']

    def find_user_id_by_comment_id(self, comment_id):
        find = {'_id': ObjectId(comment_id)}
        projection = {'_id': False, 'user_id': True}

        return self.db.comment.find_one(find, projection)['user_id']

    def find_user_id_by_post_id(self, post_id):
        find = {'_id': ObjectId(post_id)}
        projection = {'_id': False, 'user_id': True}

        return self.db.post.find_one(find, projection)['user_id']
