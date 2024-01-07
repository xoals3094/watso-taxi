import exceptions
from datetime import datetime
from bson import ObjectId
from logic.user.application.port.outgoing.TokenDao import TokenDao


class MongoDBTokenDao(TokenDao):
    def __init__(self, mongodb_connection):
        self.db = mongodb_connection['auth']

    def find_token_by_user_id(self, user_id):
        find = {'user._id': user_id}
        token = self.db.token.find_one(find)
        if token is None:
            raise exceptions.NotExistResource
        return token

    def find_token_by_refresh_token(self, refresh_token):
        find = {'refresh_token': refresh_token}
        token = self.db.token.find_one(find)
        if token is None:
            raise exceptions.NotExistResource
        return token

    def save(self, user_id, access_token, refresh_token):
        find = {'_id': user_id}
        user = self.db.user.find_one(find)

        data = {
            'user': user,
            'access_token': access_token,
            'refresh_token': refresh_token,
            'last_refreshed_date': datetime.now()
        }

        _id = self.db.token.insert_one(data)

        data = {
            'user_id': user_id,
            'token_id': _id.inserted_id,
            'device_token': None,
            'notification_allow': True,
            'last_updated_date': datetime.now()
        }

        self.db.device.insert_one(data)

    def delete(self, access_token):
        find = {'access_token': access_token}
        token = self.db.token.find_one(find)

        find = {'_id': token['_id']}
        self.db.token.delete_one(find)

        find = {'token_id': token['_id']}
        self.db.device.delete_one(find)

    def update_access_token(self, user_id, access_token):
        find = {'user._id': user_id}
        update = {
            '$set': {
                'access_token': access_token,
                'last_refreshed_date': datetime.now()
            }
        }

        self.db.token.update_one(find, update)
