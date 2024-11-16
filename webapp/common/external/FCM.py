import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging
from config.setting import CRED_PATH

cred = credentials.Certificate(CRED_PATH)
app = firebase_admin.initialize_app(cred)


def send_multicast_message(json, tokens, title=None, body=None):
    if len(tokens) == 0:
        return

    message = messaging.MulticastMessage(
        tokens=tokens,
        notification=messaging.Notification(title=title, body=body),
        data=json
    )
    result = messaging.send_each_for_multicast(message)
