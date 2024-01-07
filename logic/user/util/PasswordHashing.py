import bcrypt


def pw_hashing(pw):
    hashed_pw = bcrypt.hashpw(pw.encode('utf-8'), bcrypt.gensalt())
    hashed_pw = hashed_pw.decode('utf-8')
    return hashed_pw
