from datetime import datetime
from domain.taxi_group.core.status import Status


class TaxiGroup:
    def __init__(self,
                 group_id: int,
                 fee: int, status: Status,
                 depart_datetime: datetime,
                 depart_location_id: int,
                 arrive_location_id: int):
        self.group_id = group_id
        self.fee = fee
        self.status = status
        self.depart_datetime = depart_datetime
        self.depart_location_id = depart_location_id
        self.arrive_location_id = arrive_location_id

    @staticmethod
    def create(group_id: int, depart_datetime: datetime, depart_location_id: int, arrive_location_id: int):
        return TaxiGroup(group_id=group_id,
                         fee=6200,
                         status=Status.RECRUITING,
                         depart_datetime=depart_datetime,
                         depart_location_id=depart_location_id,
                         arrive_location_id=arrive_location_id)
