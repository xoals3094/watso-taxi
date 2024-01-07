import bcrypt


class User:
    def __init__(self, id, name, username, password, nickname, email):
        self.id = id
        self.name = name
        self.username = username
        self.password = password
        self.nickname = nickname
        self.email = email

    def compare_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    @property
    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'username': self.username,
            'password': self.password,
            'nickname': self.nickname,
            'email': self.email
        }