import random

LENGTH = 8
NUMBER_POOL = "0123456789"
ALPHABET_POOL = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
SPECIAL_POOL = "~!@#$%^&"
STRING_POOL = NUMBER_POOL + ALPHABET_POOL + SPECIAL_POOL


def generate_temp_password():
    char_list = []
    char_list.append(random.choice(NUMBER_POOL))
    char_list.append(random.choice(ALPHABET_POOL))
    char_list.append(random.choice(SPECIAL_POOL))

    for i in range(LENGTH - 3):
        char_list.append(random.choice(STRING_POOL))

    random.shuffle(char_list)

    temp_password = "".join(char_list)
    return temp_password
