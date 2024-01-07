from logic.common.push_message.application.port.outgoing.MessagePusher import MessagePusher
import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging
from config.production.config import CRED_PATH

cred = credentials.Certificate(CRED_PATH)
firebase_admin.initialize_app(cred)


class FirebaseMessagePusher(MessagePusher):
    def send(self, data, tokens):
        message = messaging.MulticastMessage(
            tokens=tokens,
            notification=messaging.Notification(data['title'], data['body']),
            data=data
        )
        result = messaging.send_multicast(message)
