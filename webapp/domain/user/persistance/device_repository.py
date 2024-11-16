from webapp.common.database import MySqlDatabase
from webapp.domain.user.entity.device import Device


class DeviceRepository(MySqlDatabase):
    def save(self, device: Device):
        self.session.add(device)
