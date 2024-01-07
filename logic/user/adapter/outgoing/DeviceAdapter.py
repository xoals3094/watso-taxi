from datetime import datetime
import exceptions
from logic.user.application.port.outgoing.DeviceDao import DeviceDao


class MongoDBDeviceDao(DeviceDao):
    def __init__(self, mongodb_connection):
        self.db = mongodb_connection['auth']

    def find_notification_allow_by_device_token(self, access_token):
        find = {'access_token': access_token}
        token = self.db.token.find_one(find)

        find = {'token_id': token['_id']}
        device = self.db.device.find_one(find)

        if device is None:
            raise exceptions.NotExistResource

        return device['notification_allow']

    def update_device_token(self, access_token, device_token):
        find = {'access_token': access_token}
        token = self.db.token.find_one(find)

        find = {'token_id': token['_id']}
        data = {
            '$set': {
                'device_token': device_token,
                'last_updated_date': datetime.now()
            }
        }
        self.db.device.update_one(find, data)

    def update_notification_allow(self, access_token, allow):
        find = {'access_token': access_token}
        token = self.db.token.find_one(find)

        find = {'token_id': token['_id']}
        data = {
            '$set': {
                'notification_allow': allow
            }
        }

        self.db.device.update_one(find, data)
