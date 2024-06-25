from pymysql import connect
from typing import List
from domain.taxi_group.dto.location import Location


class MySQLTaxiGroupQueryDao:
    def __init__(self, mysql_connection: connect):
        self.mysql_connection = mysql_connection

    def find_locations(self) -> List[Location]:
        pass

    def find_groups(self, user_id, depart_location_id, arrive_location_id, depart_datetime):
        pass

    def find_group(self, group_id):
        pass
