from datetime import datetime, timedelta
from webapp.common.schema.models import TokenModel
from webapp.common.util.token_generator import create_access_token, create_refresh_token
from webapp.common.util.id_generator import create_id


class Token(TokenModel):
    def refresh(self, exp: datetime):
        self.access_token = create_access_token(self.user_id)
        if exp - datetime.now() < timedelta(days=30):
            self.refresh_token = create_refresh_token(self.id)

    @staticmethod
    def create(user_id: str):
        token_id = create_id()
        current_datetime = datetime.now()

        return Token(
            id=token_id,
            user_id=user_id,
            access_token=create_access_token(user_id),
            refresh_token=create_refresh_token(token_id),
            created_at=current_datetime,
            updated_at=current_datetime
        )
