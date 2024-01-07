from logic.common.push_message.application.port.outgoing.TokenQueryDao import TokenQueryDao


class MongoDBTokenQueryDao(TokenQueryDao):
    def __init__(self, mongodb_connection):
        self.db = mongodb_connection['auth']

    def find_all_device_token_token_by_user_id(self, users):
        find = {
            'user_id': {'$in': users},
            'notification_allow': True,
            'device_token': {'$ne': None}
        }
        projection = {'_id': False, 'device_token': True}

        tokens = list(set([device['device_token'] for device in self.db.device.find(find, projection)]))
        return tokens

    def find_device_token_by_user_id(self, user_id):
        find = {
            'user_id': user_id,
            'notification_allow': True,
            'device_token': {'$ne': None}
        }
        projection = {'_id': False, 'device_token': True}

        tokens = list(set([device['device_token'] for device in self.db.device.find(find, projection)]))
        return tokens
