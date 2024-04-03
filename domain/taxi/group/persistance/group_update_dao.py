# review

from bson import ObjectId


class MongoDBGroupUpdateDao:
    def __init__(self, mongodb_connection):
        self.db = mongodb_connection['watso']

    def update_notice(self, group_id, notice):
        find = {'_id': ObjectId(group_id)}
        update = {'$set': {'notice': notice}}
        self.db.group.update_one(find, update)

    def update_status(self, group_id, status):
        find = {'_id': ObjectId(group_id)}
        update = {'$set': {'status': status}}
        self.db.group.update_one(find, update)

    def update_members(self, group_id, members):
        find = {'_id': ObjectId(group_id)}
        update = {'$set': {'member.members': [ObjectId(member) for member in members]}}
        self.db.group.update_one(find, update)
