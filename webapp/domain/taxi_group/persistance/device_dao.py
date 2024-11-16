from sqlalchemy import select
from webapp.common.database import MySqlDatabase
from webapp.domain.user.entity.device import Device


class DeviceDao(MySqlDatabase):
    def find_tokens_by_users(self, users: list[str]) -> list[str]:
        stmt = select(Device.fcm_token).filter(Device.user_id.in_(users))
        tokens = list(self.session.execute(stmt).scalars().all())

        return tokens
