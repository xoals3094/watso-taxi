from logic.user.application.port.incoming.DeviceUseCase import DeviceUseCase
from logic.user.application.port.outgoing.DeviceDao import DeviceDao
import exceptions


class DeviceService(DeviceUseCase):
    def __init__(self, device_dao: DeviceDao):
        self.device_dao = device_dao

    def get_notification_allow(self, access_token):
        try:
            allow = self.device_dao.find_notification_allow_by_device_token(access_token)
        except exceptions.NotExistResource:
            raise exceptions.DeviceNotFound
        return allow

    def update_device_token(self, access_token, device_token):
        self.device_dao.update_device_token(access_token, device_token)

    def update_notification_allow(self, access_token, allow):
        self.device_dao.update_notification_allow(access_token, allow)
