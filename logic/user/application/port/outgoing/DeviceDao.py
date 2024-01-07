from abc import *


class DeviceDao(metaclass=ABCMeta):
    @abstractmethod
    def find_notification_allow_by_device_token(self, access_token):
        pass

    @abstractmethod
    def update_device_token(self, access_token, device_token):
        pass

    @abstractmethod
    def update_notification_allow(self, access_token, allow):
        pass
