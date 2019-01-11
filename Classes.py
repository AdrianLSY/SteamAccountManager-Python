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

    def set_username(self, username):
        self.__username = username

    def get_password(self):
        return self.__password

    def set_password(self, password):
        self.__password = password

    def get_shared_secret(self):
        return self.__shared_secret

    def set_shared_secret(self, shared_secret):
        self.__shared_secret = shared_secret

    def is_last_used(self):
        return self.__last_used

    def set_last_used(self, boolean):
        self.__last_used = boolean
