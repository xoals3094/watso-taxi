from logic.taxi.post.domain.Post import Post, Point, Member
from logic.taxi.post.domain.Status import Status


class PointMapper:
    @staticmethod
    def point_mapping(json) -> Point:
        point = Point(depart_point_id=json['depart_point']['_id'],
                      arrive_point_id=json['arrive_point']['_id'])

        return point


class MemberMapper:
    @staticmethod
    def member_mapping(member_json) -> Member:
        members = [str(member) for member in member_json['members']]
        member = Member(max_member=member_json['max_member'],
                        members=members)

        return member


class PostMapper:
    @staticmethod
    def post_mapping(post_json) -> Post:
        post = Post(id=str(post_json['_id']),
                    owner_id=str(post_json['owner']['_id']),
                    point=PointMapper.point_mapping(post_json['point']),
                    depart_datetime=post_json['depart_datetime'],
                    status=Status(post_json['status']),
                    fee=post_json['fee'],
                    member=MemberMapper.member_mapping(post_json['member']),
                    notice=post_json['notice'])

        return post
