import hashlib
from database.db import DataBase
from models.user import User

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

class AuthService:
    def __init__(self):
        self.db = DataBase()

    def login(self, username, password):
        hashed = hash_password(password)

        rows = self.db.execute(
            "SELECT id, username, role FROM users WHERE username=? AND password=?",
            (username, hashed),
            fetch=True
        )

        if rows:
            return User(*rows[0])
        return None
    def ensure_admin_exists(self):
      rows = self.db.execute(
          "SELECT id FROM users WHERE role = 'admin'",
          fetch=True
      )

      if not rows:
          self.db.execute(
              "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
              ("admin", hash_password("admin123"), "admin")
          )