from typing import List
from bson import ObjectId
import pymongo

from logic.taxi.post.dto.PostSummaryDto import PostSummaryDto
from logic.taxi.post.dto.PostDetailDto import PostDetailDto
from logic.taxi.post.application.port.outgoing.PostQueryDao import PostQueryDao
from datetime import datetime
import exceptions


class MongoDBPostQueryDao(PostQueryDao):
    def __init__(self, mongodb_connection):
        self.db = mongodb_connection['taxi']

    def find_joinable_posts_by_user_id(self, user_id) -> List[PostSummaryDto]:
        find = {
            'depart_time': {'$gte': datetime.now()},
            'status': 'RECRUITING',
            'users': {'$ne': user_id}
        }

        posts_json = self.db.post.find(find).sort("depart_time", pymongo.ASCENDING)
        return [PostSummaryDto.mapping(post_json) for post_json in posts_json]

    def find_joined_posts_by_user_id(self, user_id) -> List[PostSummaryDto]:
        find = {
            'status': {'$in': ['RECRUITING', 'CLOSED', 'BOARDING', 'SETTLE']},
            'users': {'$eq': user_id}
        }

        posts_json = self.db.post.find(find).sort("depart_time", pymongo.ASCENDING)
        return [PostSummaryDto.mapping(post_json) for post_json in posts_json]

    def find_all_posts_by_user_id(self, user_id) -> List[PostSummaryDto]:
        find = {
            'users': {'$eq': user_id},
            'status': {'$in': ['COMPLETION', 'CANCELED']}
        }
        posts_json = self.db.post.find(find).sort("depart_time", pymongo.DESCENDING)

        return [PostSummaryDto.mapping(post_json) for post_json in posts_json]

    def find_post_by_id(self, post_id) -> PostDetailDto:
        find = {'_id': ObjectId(post_id)}
        post_json = self.db.post.find_one(find)

        if post_json is None:
            raise exceptions.NotExistPost

        return PostDetailDto.mapping(post_json)
