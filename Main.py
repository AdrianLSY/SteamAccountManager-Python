import os
import autoit
import json
import time
import hmac
import struct
import base64
from hashlib import sha1
from Classes import *

accounts = List()


def read_json():
    try:
        json.loads(open('accounts.json').read())
    except FileNotFoundError:
        open("accounts.json", "x")
    for user in json.loads(open('accounts.json').read()):
        accounts.add_user(User(
            user['username'],
            user['password'],
            user['shared_secret'],
            user['last_used']
        ))


def write_json():
    data = []
    with open('accounts.json', 'w') as outfile:
        for user in accounts.get_users():
            data.append({
                'username': user.get_username(),
                'password': user.get_password(),
                'shared_secret': user.get_shared_secret(),
                'last_used': user.is_last_used()
            })
        json.dump(data, outfile)


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


def use_last_used():
    if accounts.get_last_used() is not None:
        log_in(accounts.get_last_used())


def select_account():
    print('Select User : ( + to add, - to remove)')
    i = 1
    for user in accounts.get_users():
        print("{}. {}".format(i, user.get_username()))
        i += 1
    while True:
        try:
            selection = input('Selection : ')
            if selection == '+':
                create_account()
                return
            if selection == '-':
                delete_account()
                return
            log_in(accounts.use_specified(int(selection) - 1))
            break
        except (ValueError, IndexError):
            print('Invalid Input')
    write_json()


def create_account():
    def not_none(key):
        while True:
            if key == 'username':
                user_input = input('Username : ')
            if key == 'password':
                user_input = input('Password : ')
            if user_input is not '':
                break
            print('Please enter a {}'.format(key))
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
    write_json()


def delete_account():
    selection = int(input('Select an account to remove : '))
    accounts.delete_user(selection - 1)
    write_json()


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
