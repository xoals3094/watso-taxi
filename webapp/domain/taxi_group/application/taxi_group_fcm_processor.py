from webapp.common.external import FCM
from webapp.domain.taxi_group.persistance.device_dao import DeviceDao


class TaxiGroupFCMProcessor:
    def __init__(self, device_dao: DeviceDao):
        self.device_dao = device_dao

    def settle(self, group_id: str, users: list[str]):
        tokens = self.device_dao.find_tokens_by_users(users)
        json = {'group_id': group_id}
        FCM.send_multicast_message(
            title='정산을 시작합니다!',
            json=json,
            tokens=tokens
        )

    def complete(self, group_id: str, users: list[str]):
        tokens = self.device_dao.find_tokens_by_users(users)
        json = {'group_id': group_id}
        FCM.send_multicast_message(
            title='정산 완료!',
            json=json,
            tokens=tokens
        )