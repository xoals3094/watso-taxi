from logic.taxi.post.domain.Post import Post


class PostMapper:
    @staticmethod
    def post_mapping(post_json) -> Post:
        post = Post(id=str(post_json['_id']),
                    user_id=str(post_json['user']['_id']),
                    status=post_json['status'],
                    direction=post_json['direction'],
                    depart_time=post_json['depart_time'],
                    max_member=post_json['max_member'],
                    content=post_json['content'],
                    users=[str(user_id) for user_id in post_json['users']])

        return post
