import unittest
from bson import ObjectId
from datetime import datetime
from exceptions import AuthenticationException, DomainException
from domain.group import Group, Point, Member
from domain.taxi_group.entity.status import Status


class GroupCheckOwnerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.owner_id = str(ObjectId())

        point = Point(depart_point_id=str(ObjectId()), arrive_point_id=str(ObjectId()))
        member = Member(max_member=4, members=[self.owner_id])

        self.group = Group(id=str(ObjectId()),
                           owner_id=self.owner_id,
                           point=point,
                           depart_datetime=datetime.now(),
                           status=Status.RECRUITING,
                           fee=6200,
                           member=member,
                           notice='테스트')

    def test_validation_success(self):
        self.group.check_owner(user_id=self.owner_id)

    def test_check_owner_fail(self):
        with self.assertRaises(AuthenticationException.AccessDeniedException):
            self.group.check_owner(user_id=str(ObjectId()))


class GroupParticipateTest(unittest.TestCase):
    def setUp(self) -> None:
        self.owner_id = str(ObjectId())
        self.point = Point(depart_point_id=str(ObjectId()), arrive_point_id=str(ObjectId()))

    def test_participate_success(self):
        member = Member(max_member=4, members=[self.owner_id])
        group = Group(id=str(ObjectId()),
                      owner_id=self.owner_id,
                      point=self.point,
                      depart_datetime=datetime.now(),
                      status=Status.RECRUITING,
                      fee=6200,
                      member=member,
                      notice='테스트')

        user_id = str(ObjectId())
        group.participate(user_id)

        self.assertIn(user_id, group.member.members)

    def test_exceed_max_member(self):
        member = Member(max_member=2, members=[self.owner_id, str(ObjectId())])
        group = Group(id=str(ObjectId()),
                      owner_id=self.owner_id,
                      point=self.point,
                      depart_datetime=datetime.now(),
                      status=Status.RECRUITING,
                      fee=6200,
                      member=member,
                      notice='테스트')

        user_id = str(ObjectId())
        msg = '현재 인원이 최대 인원에 도달하여 참여가 불가능합니다. 2/2'
        with self. assertRaises(DomainException.ParticipationFailedException) as e:
            group.participate(user_id)
        self.assertEqual(msg, str(e.exception))

    def test_already_participation(self):
        user_id = str(ObjectId())
        member = Member(max_member=4, members=[self.owner_id, user_id])
        group = Group(id=str(ObjectId()),
                      owner_id=self.owner_id,
                      point=self.point,
                      depart_datetime=datetime.now(),
                      status=Status.RECRUITING,
                      fee=6200,
                      member=member,
                      notice='테스트')

        msg = '참여가 완료된 사용자입니다.'
        with self.assertRaises(DomainException.ParticipationFailedException) as e:
            group.participate(user_id)
        self.assertEqual(msg, str(e.exception))


class GroupLeaveTest(unittest.TestCase):
    def setUp(self) -> None:
        self.owner_id = str(ObjectId())
        self.point = Point(depart_point_id=str(ObjectId()), arrive_point_id=str(ObjectId()))

    def test_leave_success(self):
        user_id = str(ObjectId())
        member = Member(max_member=4, members=[self.owner_id, user_id])
        group = Group(id=str(ObjectId()),
                      owner_id=self.owner_id,
                      point=self.point,
                      depart_datetime=datetime.now(),
                      status=Status.RECRUITING,
                      fee=6200,
                      member=member,
                      notice='테스트')

        group.leave(user_id)
        self.assertNotIn(user_id, group.member.members)

    def test_owner_leave(self):
        member = Member(max_member=4, members=[self.owner_id])
        group = Group(id=str(ObjectId()),
                      owner_id=self.owner_id,
                      point=self.point,
                      depart_datetime=datetime.now(),
                      status=Status.RECRUITING,
                      fee=6200,
                      member=member,
                      notice='테스트')

        msg = '대표 유저는 게시글 탈퇴가 불가능합니다.'
        with self. assertRaises(DomainException.LeaveFailedException) as e:
            group.leave(self.owner_id)
        self.assertEqual(msg, str(e.exception))

    def test_not_participate_member(self):
        member = Member(max_member=4, members=[self.owner_id])
        group = Group(id=str(ObjectId()),
                      owner_id=self.owner_id,
                      point=self.point,
                      depart_datetime=datetime.now(),
                      status=Status.RECRUITING,
                      fee=6200,
                      member=member,
                      notice='테스트')

        msg = '참여하지 않은 사용자입니다.'
        with self.assertRaises(DomainException.LeaveFailedException) as e:
            group.leave(str(ObjectId()))
        self.assertEqual(msg, str(e.exception))
