from webapp.common.exceptions import persistence
from webapp.domain.chat.chat import Channel


class ChannelManager:
    def __init__(self):
        self.channels: dict[str, Channel] = {}

    def get_channel(self, group_id) -> Channel:
        try:
            channel = self.channels[group_id]
        except KeyError:
            raise persistence.ResourceNotFound

        return channel

    def create_channel(self, group_id) -> Channel:
        channel = Channel(group_id)
        self.channels[group_id] = channel

        return channel
