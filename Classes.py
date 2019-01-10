import time
import hmac
import struct
import base64
from hashlib import sha1


class List:
    def __init__(self):
        self.__users = []

    def get_users(self):
        return self.__users

    def add_user(self, user):
        self.__users.append(user)

    def delete_user(self, selection):
        del self.__users[selection]

    def get_last_used(self):
        for objects in self.__users:
            if objects.is_last_used():
                return objects
        return None

    def use_specified(self, selection):
        if self.get_last_used() is not None:
            self.get_last_used().set_last_used(False)
        self.__users[selection].set_last_used(True)
        return self.__users[selection]


class User:
    def __init__(self, username, password, shared_secret, last_used):
        self.__username = username
        self.__password = password
        self.__shared_secret = shared_secret
        self.__last_used = last_used

    def get_username(self):
        return self.__username

    def get_username_sanitized(self):
        return self.bash_sanitized(self.__username)

    def set_username(self, username):
        self.__username = username

    def get_password(self):
        return self.__password

    def get_password_sanitized(self):
        return self.bash_sanitized(self.__password)

    def set_password(self, password):
        self.__password = password

    def get_shared_secret(self):
        return self.__shared_secret

    def set_shared_secret(self, shared_secret):
        try:
            self.__shared_secret = shared_secret
            self.generate_auth_code()
        except:
            self.__shared_secret = None
            return False

    def is_last_used(self):
        return self.__last_used

    def set_last_used(self, boolean):
        self.__last_used = boolean

    def generate_auth_code(self, timestamp: int = None) -> str:
        if self.__shared_secret is not None:
            if timestamp is None:
                timestamp = int(time.time())
            time_buffer = struct.pack('>Q', timestamp // 30)  # pack as Big endian, uint64
            time_hmac = hmac.new(base64.b64decode(self.__shared_secret), time_buffer, digestmod=sha1).digest()
            begin = ord(time_hmac[19:20]) & 0xf
            full_code = struct.unpack('>I', time_hmac[begin:begin + 4])[0] & 0x7fffffff
            characters = '23456789BCDFGHJKMNPQRTVWXY'
            auth_code = ''
            for _ in range(5):
                full_code, i = divmod(full_code, len(characters))
                auth_code += characters[i]
            return auth_code
        return None

    def bash_sanitized(self, string):
        characters = {'^': '^', '&': '^', '<': '^', '>': '^', '|': '^'}
        string = list(string)
        for i in range(len(string)):
            if string[i] in characters:
                string[i] = '{}{}'.format(characters[string[i]], string[i])
        return ''.join(string)
