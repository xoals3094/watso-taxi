import random

LENGTH = 4
STRING_POOL = "0123456789"


def generate_auth_code():
    auth_code = ""
    for i in range(LENGTH):
        auth_code += random.choice(STRING_POOL)

    return auth_code