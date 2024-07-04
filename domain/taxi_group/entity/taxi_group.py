from datetime import datetime
from domain.taxi_group.entity.status import Status
from exceptions import DomainException


class TaxiGroup:
    def __init__(self,
                 group_id: int,
                 fee: int,
                 status: Status,
                 depart_datetime: datetime,
                 direction: str):
        self.group_id = group_id
        self.fee = fee
        self.status = status
        self.depart_datetime = depart_datetime
        self.direction = direction

    def set_status(self, status: Status):
        self.status.to(status)
        self.status = status

    def verify_fee(self, total_cost: int):
        if total_cost != self.fee:
            raise DomainException.VerifyFailException(
                msg=f'비용이 일치하지 않습니다 fee={self.fee} total_cost={total_cost}'
            )

    @staticmethod
    def create(group_id: int, depart_datetime: datetime, direction):
        return TaxiGroup(group_id=group_id,
                         fee=6200,
                         status=Status.RECRUITING,
                         depart_datetime=depart_datetime,
                         direction=direction)

    @staticmethod
    def mapping(json):
        return TaxiGroup(group_id=json['group_id'],
                         fee=json['fee'],
                         status=json['status'],
                         depart_datetime=json['depart_datetime'],
                         direction=json['direction'])
