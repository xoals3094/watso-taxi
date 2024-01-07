from dependency_injector.wiring import inject, Provide
from src.common_container import CommonContainer
from logic.common.push_message.application.port.outgoing.UserIdFinder import UserIdFinder
from logic.common.push_message.application.port.outgoing.TokenQueryDao import TokenQueryDao
from logic.common.push_message.application.port.outgoing.MessagePusher import MessagePusher
import exceptions

from blinker import signal

comment_event = signal('comment-event')


@comment_event.connect_via('created')
@inject
def push_comment_message(sender, parent_id, user_id, nickname, content, post_id,
                         user_id_finder: UserIdFinder = Provide[CommonContainer.user_id_finder],
                         token_query_dao: TokenQueryDao = Provide[CommonContainer.token_query_dao],
                         message_pusher: MessagePusher = Provide[CommonContainer.message_pusher]):

    if parent_id is None:
        post_owner_id = user_id_finder.find_user_id_by_post_id(post_id)

        tokens = token_query_dao.find_device_token_by_user_id(post_owner_id)
        data = {
            'title': f'{nickname}님의 댓글',
            'body': f'{content}',
            'post_id': post_id
        }
        message_pusher.send(data, tokens)
        return

    parent_comment_owner_id = user_id_finder.find_user_id_by_comment_id(parent_id)
    if user_id == parent_comment_owner_id:
        return

    tokens = token_query_dao.find_device_token_by_user_id(parent_comment_owner_id)
    data = {
        'title': f'{nickname}님의 답글',
        'body': f'{content}',
        'post_id': post_id
    }

    message_pusher.send(data, tokens)
