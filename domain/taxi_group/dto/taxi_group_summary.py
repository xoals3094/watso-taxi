from datetime import datetime

class GroupSummary:
    def __init__(self, ):


class TaxiGroupSummary:
    def __init__(self,
                 group_id: int,
                 fee: int,
                 status: str,
                 depart_datetime: datetime,
                 depart_location_id: int,
                 arrive_location_id: int):
        self.group_id = group_id
        self.fee = fee
        self.status = status
        self.depart_datetime = depart_datetime
        self.depart_location_id = depart_location_id
        self.arrive_location_id = arrive_location_id
