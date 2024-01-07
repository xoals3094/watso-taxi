from dependency_injector.wiring import inject, Provide
from src.common_container import CommonContainer
from logic.common.push_message.application.port.outgoing.TokenQueryDao import TokenQueryDao
from logic.common.push_message.application.port.outgoing.MessagePusher import MessagePusher
import exceptions

from blinker import signal

post_event = signal('post-event')


@post_event.connect_via('joined')
@inject
def push_joined_message(sender, owner_user_id, current_member, store_id, post_id, user_id, nickname, order_json,
                        token_query_dao: TokenQueryDao = Provide[CommonContainer.token_query_dao],
                        message_pusher: MessagePusher = Provide[CommonContainer.message_pusher]):

    tokens = token_query_dao.find_device_token_by_user_id(owner_user_id)
    data = {
        'title': f'{nickname}님이 참여했습니다!',
        'body': f'현재까지 {current_member}명 참여했습니다!',
        'post_id': post_id
    }

    message_pusher.send(data, tokens)


@post_event.connect_via('ordered')
@inject
def push_ordered_message(sender, users, post_id,
                         token_query_dao: TokenQueryDao = Provide[CommonContainer.token_query_dao],
                         message_pusher: MessagePusher = Provide[CommonContainer.message_pusher]):
    tokens = token_query_dao.find_all_device_token_token_by_user_id(users)

    data = {
        'title': '주문이 완료되었습니다!',
        'body': '조금만 기다려주세요!',
        'post_id': post_id
    }

    message_pusher.send(data, tokens)


@post_event.connect_via('delivered')
@inject
def push_delivered_message(sender, users, place, post_id,
                           token_query_dao: TokenQueryDao = Provide[CommonContainer.token_query_dao],
                           message_pusher: MessagePusher = Provide[CommonContainer.message_pusher]):
    tokens = token_query_dao.find_all_device_token_token_by_user_id(users)

    data = {
        'title': '배달이 완료되었습니다!',
        'body': f'{place}로 와주세요!',
        'post_id': post_id
    }

    message_pusher.send(data, tokens)
