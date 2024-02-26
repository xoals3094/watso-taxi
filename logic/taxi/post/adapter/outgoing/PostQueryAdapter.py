from typing import List
from bson import ObjectId
import pymongo
from logic.taxi.post.domain.Status import Status

from logic.taxi.post.dto.PostSummaryDto import PostSummaryDto
from logic.taxi.post.dto.PostDetailDto import PostDetailDto
from logic.taxi.post.application.port.outgoing.PostQueryDao import PostQueryDao
from exceptions import PersistenceException


class MongoDBPostQueryDao(PostQueryDao):
    def __init__(self, mongodb_connection):
        self.db = mongodb_connection['watso']

    def find_posts(self, user_id, depart_point_id, arrive_point_id, depart_datetime) -> List[PostSummaryDto]:
        find = {
            'point.depart_point._id': ObjectId(depart_point_id),
            'point.arrive_point._id': ObjectId(arrive_point_id),
            'depart_datetime': {'$gte': depart_datetime},
            'status': Status.RECRUITING,
        }
        posts_json = self.db.post.find(find).sort("depart_datetime", pymongo.ASCENDING)
        return [PostSummaryDto.mapping(post_json) for post_json in posts_json]

    def find_post_by_id(self, post_id) -> PostDetailDto:
        find = {'_id': ObjectId(post_id)}
        post_json = self.db.post.find_one(find)

        if post_json is None:
            raise PersistenceException.ResourceNotFoundException(
                msg=f"게시글 정보를 찾을 수 없습니다 id={post_id}"
            )

        return PostDetailDto.mapping(post_json)
