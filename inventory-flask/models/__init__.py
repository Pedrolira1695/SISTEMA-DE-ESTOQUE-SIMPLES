class UserModel:
    def __init__(self):
        self.users = {"admin": "admin"}  # Usuário padrão

    def register(self, username, password):
        if username in self.users:
            return False
        self.users[username] = password
        return True

    def authenticate(self, username, password):
        return self.users.get(username) == password
