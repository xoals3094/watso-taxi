from pymysql import connect
from domain.taxi_group.entity.taxi_group import TaxiGroup
from domain.taxi_group.core.status import Status


class MySQLTaxiGroupDao:
    def __init__(self, mysql_connection: connect):
        self.cursor = mysql_connection.cursor()

    def insert(self, taxi_group: TaxiGroup):
        pass

    def update_status(self, status: Status):
        pass

    def find_status_by_id(self, group_id) -> Status:
        pass
