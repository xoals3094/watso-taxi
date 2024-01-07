class PostDetailDto:
    def __init__(self, id, user, status, direction, depart_time, max_member, content, users):
        self.id = id
        self.user = user
        self.status = status
        self.direction = direction
        self.depart_time = depart_time
        self.max_member = max_member
        self.content = content
        self.users = users

    @property
    def json(self):
        return {
            'id': self.id,
            'user': self.user,
            'status': self.status,
            'direction': self.direction,
            'depart_time': self.depart_time,
            'max_member': self.max_member,
            'content': self.content,
            'users': self.users
        }

    @staticmethod
    def mapping(post_json):
        user = {
            'id': str(post_json['user']['_id']),
            'nickname': post_json['user']['nickname']
        }
        return PostDetailDto(id=str(post_json['_id']),
                             user=user,
                             status=post_json['status'],
                             direction=post_json['direction'],
                             depart_time=post_json['depart_time'],
                             max_member=post_json['max_member'],
                             content=post_json['content'],
                             users=[str(user_id) for user_id in post_json['users']])
