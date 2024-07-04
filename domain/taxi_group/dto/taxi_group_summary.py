from datetime import datetime


class TaxiGroupSummary:
    def __init__(self,
                 group_id: int,
                 fee: int,
                 status: str,
                 depart_datetime: datetime,
                 direction: str):
        self.group_id = group_id
        self.fee = fee
        self.status = status
        self.depart_datetime = depart_datetime
        self.direction = direction
