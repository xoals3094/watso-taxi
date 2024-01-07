import pymongo.errors
from pymongo import MongoClient
import exceptions
from logic.auth.application.port.outgoing.UserRepository import UserRepository

from logic.auth.domain.User import User


class MongoDBUserRepository(UserRepository):
    def __init__(self, mongodb_connection: MongoClient):
        self.db = mongodb_connection['auth']

    def find_user_by_id(self, user_id) -> User:
        find = {'_id': user_id}
        user_json = self.db.user.find_one(find)

        if user_json is None:
            raise exceptions.NotExistResource

        return User(id=user_json['_id'],
                    name=user_json['name'],
                    nickname=user_json['nickname'],
                    username=user_json['username'],
                    password=user_json['password'],
                    email=user_json['email'])

    def find_user_by_username(self, username) -> User:
        find = {'username': username}
        user_json = self.db.user.find_one(find)

        if user_json is None:
            raise exceptions.NotExistResource

        return User(id=user_json['_id'],
                    name=user_json['name'],
                    nickname=user_json['nickname'],
                    username=user_json['username'],
                    password=user_json['password'],
                    email=user_json['email'])

    def find_user_by_email(self, email) -> User:
        find = {'email': email}
        user_json = self.db.user.find_one(find)

        if user_json is None:
            raise exceptions.NotExistResource

        return User(id=user_json['_id'],
                    name=user_json['name'],
                    nickname=user_json['nickname'],
                    username=user_json['username'],
                    password=user_json['password'],
                    email=user_json['email'])

    def save(self, user: User):
        try:
            self.db.user.insert_one(user.json)
        except pymongo.errors.DuplicateKeyError:
            raise exceptions.DuplicateKeyError

    def delete(self, user_id):
        find = {'_id': user_id}
        self.db.user.delete_one(find)
