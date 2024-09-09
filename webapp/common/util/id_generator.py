from datetime import datetime


def create_id():
    return int(datetime.now().timestamp() * 1000)