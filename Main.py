import os
import hmac
import time
import uuid
import autoit
import base64
import pickle
import struct
from Classes import *
from hashlib import sha1
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet


def obtain_keys():
    try:
        accounts = pickle.load(open('accounts.dat', 'rb'))
        key = generate_key(open('salt.dat', 'rb').read())
    except FileNotFoundError:
        open('accounts.dat', 'x')
        open('salt.dat', 'x')
        accounts = List()
        salt = os.urandom(16)
        key = generate_key(salt)
        pickle.dump(accounts, open('accounts.dat', 'wb'), pickle.HIGHEST_PROTOCOL)
        with open('salt.dat', 'wb') as outfile:
            outfile.write(salt)
        return key, accounts
    return key, accounts


def read_data(key, accounts):
    if accounts.get_users() is not None:
        for user in accounts.get_users():
            user.set_username(decrypt(key, user.get_username()))
            user.set_password(decrypt(key, user.get_password()))
            if user.get_shared_secret() is not None:
                user.set_shared_secret(decrypt(key, user.get_shared_secret()))
    return key, accounts


def write_data(key, accounts):
    for user in accounts.get_users():
        user.set_username(encrypt(key, user.get_username()))
        user.set_password(encrypt(key, user.get_password()))
        if user.get_shared_secret() is not None:
            user.set_shared_secret(encrypt(key, user.get_shared_secret()))
    pickle.dump(accounts, open('accounts.dat', 'wb'), pickle.HIGHEST_PROTOCOL)


def log_in(user):
    os.system('taskkill /f /im Steam.exe')
    os.system('start "" "C:\Program Files (x86)\Steam\Steam.exe" -login {} {}'.format(
        batch_sanitized(user.get_username()),
        batch_sanitized(user.get_password())
    ))
    if user.get_shared_secret() is not None:
        autoit.win_wait("Steam Guard")
        autoit.win_activate("Steam Guard")
        autoit.win_wait_active("Steam Guard")
        autoit.send(generate_auth_code(user.get_shared_secret()))
        autoit.send('{ENTER}')


def use_last_used(key, accounts):
    read_data(key, accounts)
    if accounts.get_last_used() is not None:
        log_in(accounts.get_last_used())


def select_account(key, accounts):
    print('Select User : ( + to add, - to remove)')
    i = 1
    for user in accounts.get_users():
        print("{}. {}".format(i, user.get_username()))
        i += 1
    while True:
        try:
            selection = input('Selection : ')
            if selection == '+':
                return create_account(key, accounts)
            if selection == '-':
                return delete_account(key, accounts)
            log_in(accounts.use_specified(int(selection) - 1))
            break
        except (ValueError, IndexError):
            print('Invalid Input')


def create_account(key, accounts):
    def not_none(field):
        while True:
            user_input = None
            if field == 'username':
                user_input = input('Username : ')
            if field == 'password':
                user_input = input('Password : ')
            if user_input is not None:
                break
            print('Please enter a {}'.format(field))
        return user_input

    def valid_shared_secret():
        print("\n"
              "OPTIONAL : Shared_secret from Mobile Authenticator maFile\n"
              "Paste ONLY your 'shared_secret' code from your user maFile\n"
              "This will automate your SteamGuard Mobile 2FA during login\n"
              "Leave blank if none")
        while True:
            shared_secret = input('shared_secret : ')
            if shared_secret == '':
                return None
            try:
                generate_auth_code(shared_secret)
                return shared_secret
            except ValueError:
                print('Invalid shared_secret')

    accounts.add_user(User(
        not_none('username'),
        not_none('password'),
        valid_shared_secret(),
        False
    ))
    write_data(key, accounts)
    return read_data(key, accounts)


def delete_account(key, accounts):
    selection = int(input('Select an account to remove : '))
    accounts.delete_user(selection - 1)
    write_data(key, accounts)
    return read_data(key, accounts)


def generate_auth_code(shared_secret: str, timestamp: int = None) -> str:
    if timestamp is None:
        timestamp = int(time.time())
    time_buffer = struct.pack('>Q', timestamp // 30)  # pack as Big endian, uint64
    time_hmac = hmac.new(base64.b64decode(shared_secret), time_buffer, digestmod=sha1).digest()
    begin = ord(time_hmac[19:20]) & 0xf
    full_code = struct.unpack('>I', time_hmac[begin:begin + 4])[0] & 0x7fffffff
    characters = '23456789BCDFGHJKMNPQRTVWXY'
    auth_code = ''
    for _ in range(5):
        full_code, i = divmod(full_code, len(characters))
        auth_code += characters[i]
    return auth_code


def batch_sanitized(string):
    characters = {'^': '^', '&': '^', '<': '^', '>': '^', '|': '^', '"': '\\'}
    string = list(string)
    for i in range(len(string)):
        if string[i] in characters:
            string[i] = '{}{}'.format(characters[string[i]], string[i])
    return ''.join(string)


def generate_key(salt):
    return base64.urlsafe_b64encode(PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    ).derive(str(uuid.getnode()).encode()))


def encrypt(key, message):
    return Fernet(key).encrypt(message.encode())


def decrypt(key, message):
    return Fernet(key).decrypt(message).decode()
