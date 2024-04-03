# review
from domain.taxi.group.entity.group import Group, Member, Point
from domain.taxi.group.core.status import Status


class GroupEntityMapper:
    @staticmethod
    def mapping_group_entity(json) -> Group:
        point = GroupEntityMapper._mapping_point(json['point'])
        member = GroupEntityMapper._mapping_member(json['member'])
        return Group(id=str(json['_id']),
                     owner_id=str(json['owner_id']['_id']),
                     point=point,
                     depart_datetime=json['depart_datetime'],
                     status=Status(json['status']),
                     fee=json['fee'],
                     member=member,
                     notice=json['notice'])

    @staticmethod
    def _mapping_point(json):
        return Point(depart_point_id=json['depart_point']['_id'],
                     arrive_point_id=json['arrive_point']['_id'])

    @staticmethod
    def _mapping_member(json):
        return Member(max_member=json['max_member'],
                      members=[str(member_id) for member_id in json['members']])
