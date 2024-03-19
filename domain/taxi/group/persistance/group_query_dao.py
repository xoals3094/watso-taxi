from typing import List
from bson import ObjectId
import pymongo
from domain.taxi.group.core.status import Status

from domain.taxi.group.dto.response_group_detail import ResponseGroupDetail
from domain.taxi.group.dto.response_group_summary import ResponseGroupSummary
from exceptions import PersistenceException


class MongoDBGroupQueryDao:
    def __init__(self, mongodb_connection):
        self.db = mongodb_connection['watso']

    def find_groups(self, user_id, depart_point_id, arrive_point_id, depart_datetime) -> List[ResponseGroupDetail]:
        find = {
            'point.depart_point._id': ObjectId(depart_point_id),
            'point.arrive_point._id': ObjectId(arrive_point_id),
            'depart_datetime': {'$gte': depart_datetime},
            'status': Status.RECRUITING,
        }
        groups_json = self.db.post.find(find).sort("depart_datetime", pymongo.ASCENDING)
        return [ResponseGroupDetail.mapping(group_json) for group_json in groups_json]

    def find_group_by_id(self, post_id) -> ResponseGroupSummary:
        find = {'_id': ObjectId(post_id)}
        group_json = self.db.post.find_one(find)

        if group_json is None:
            raise PersistenceException.ResourceNotFoundException(
                msg=f"게시글 정보를 찾을 수 없습니다 id={post_id}"
            )

        return ResponseGroupSummary.mapping(group_json)
