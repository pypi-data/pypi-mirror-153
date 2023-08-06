from base64 import urlsafe_b64encode
from hashlib import blake2b

from cryptography.fernet import Fernet as Base


class Fernet:
    def __init__(self, psw):
        key = self.make_key(psw)
        self.fernet = Base(key)

    @staticmethod
    def make_key(psw):
        h = blake2b(digest_size=32)
        h.update(psw.encode())
        key = urlsafe_b64encode(h.digest())
        return key

    def encrypt(self, data):
        return self.fernet.encrypt(data.encode())

    def decrypt(self, data):
        return self.fernet.decrypt(data).decode()
