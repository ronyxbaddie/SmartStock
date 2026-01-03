class User:
    def __init__(self, id, username, role):
        self.id = id
        self.username = username
        self.role = role

    def is_admin(self):
        return self.role == "admin"
