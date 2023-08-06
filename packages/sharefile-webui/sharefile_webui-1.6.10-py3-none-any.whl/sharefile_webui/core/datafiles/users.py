from werkzeug.security import generate_password_hash, check_password_hash
from .base import BaseDatafile


class Users(BaseDatafile):
    def add_user(self, user: str, password: str):
        self.data[user] = generate_password_hash(password)

    def remove_user(self, user: str) -> bool:
        if user in self.data:
            del self.data[user]
            return True
        return False

    def check_user(self, user: str, password: str):
        password_hash = self.data.get(user)
        if password_hash:
            check = check_password_hash(password_hash, password)
            return user if check else None
