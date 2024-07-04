import unittest
from exceptions import DomainException
from domain.taxi_group.entity.status import Status


class StatusToTest(unittest.TestCase):
    def test_status_is_RECRUITING(self):
        not_allowed_status = [Status.BOARDING, Status.SETTLEMENT, Status.COMPLETED]

        current_status = Status.RECRUITING
        for next_status in not_allowed_status:
            with self.subTest(next_status):
                with self.assertRaises(DomainException.InvalidStateException) as e:
                    current_status.to(next_status)
                msg = f"'RECRUITING' -> '{next_status}'는 허용되지 않는 상태코드 변경입니다."
                self.assertEqual(msg, str(e.exception))

    def test_status_is_CLOSED(self):
        not_allowed_status = [Status.SETTLEMENT, Status.COMPLETED]

        current_status = Status.CLOSED
        for next_status in not_allowed_status:
            with self.subTest(next_status):
                with self.assertRaises(DomainException.InvalidStateException) as e:
                    current_status.to(next_status)
                msg = f"'CLOSED' -> '{next_status}'는 허용되지 않는 상태코드 변경입니다."
                self.assertEqual(msg, str(e.exception))

    def test_status_is_BOARDING(self):
        not_allowed_status = [Status.RECRUITING, Status.CLOSED, Status.COMPLETED]

        current_status = Status.BOARDING
        for next_status in not_allowed_status:
            with self.subTest(next_status):
                with self.assertRaises(DomainException.InvalidStateException) as e:
                    current_status.to(next_status)
                msg = f"'BOARDING' -> '{next_status}'는 허용되지 않는 상태코드 변경입니다."
                self.assertEqual(msg, str(e.exception))

    def test_status_is_SETTLEMENT(self):
        not_allowed_status = [Status.RECRUITING, Status.CLOSED, Status.BOARDING]

        current_status = Status.SETTLEMENT
        for next_status in not_allowed_status:
            with self.subTest(next_status):
                with self.assertRaises(DomainException.InvalidStateException) as e:
                    current_status.to(next_status)
                msg = f"'SETTLEMENT' -> '{next_status}'는 허용되지 않는 상태코드 변경입니다."
                self.assertEqual(msg, str(e.exception))
