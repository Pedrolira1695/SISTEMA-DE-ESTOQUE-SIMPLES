class AuthController:
    def __init__(self):
        self.users = {"admin": "admin"}

    def login(self, username, password):
        return self.users.get(username) == password

    def register(self, username, password):
        if username in self.users:
            return False
        self.users[username] = password
        return True

    def logout(self):
        pass
