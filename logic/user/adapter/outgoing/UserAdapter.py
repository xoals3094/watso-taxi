from logic.user.application.port.outgoing.UserDao import UserDao


class MongoDBUserDao(UserDao):
    def __init__(self, mongodb_connection):
        self.db = mongodb_connection['auth']

    def is_already_exist_username(self, username) -> bool:
        find = {'username': username}
        user_json = self.db.user.find_one(find)
        return user_json is not None

    def is_already_exist_nickname(self, nickname) -> bool:
        find = {'nickname': nickname}
        user_json = self.db.user.find_one(find)
        return user_json is not None

    def is_already_exist_email(self, email) -> bool:
        find = {'email': email}
        user_json = self.db.user.find_one(find)
        return user_json is not None

    def update_pw(self, user_id, pw):
        find = {'_id': user_id}
        update = {'$set': {'pw': pw}}
        self.db.user.update_many(find, update)

        find = {'user._id': user_id}
        update = {'$set': {'user.pw': pw}}
        self.db.token.update_many(find, update)

    def update_email(self, user_id, email):
        find = {'_id': user_id}
        update = {'$set': {'email': email}}
        self.db.user.update_many(find, update)

        find = {'user._id': user_id}
        update = {'$set': {'user.email': email}}
        self.db.token.update_many(find, update)

    def update_nickname(self, user_id, nickname):
        find = {'_id': user_id}
        update = {'$set': {'nickname': nickname}}
        self.db.user.update_many(find, update)

        find = {'user._id': user_id}
        update = {'$set': {'user.nickname': nickname}}
        self.db.token.update_many(find, update)

    def update_account_number(self, user_id, account_number):
        find = {'_id': user_id}
        update = {'$set': {'account_number': account_number}}
        self.db.user.update_many(find, update)

        find = {'user._id': user_id}
        update = {'$set': {'user.account_number': account_number}}
        self.db.token.update_many(find, update)

