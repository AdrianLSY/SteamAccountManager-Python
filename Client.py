import os
import autoit
import json
from Classes import *

accounts = List()


def read_json():
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
        user.get_username_sanitized(),
        user.get_password_sanitized()
    ))
    if user.get_shared_secret() is not None:
        autoit.win_wait("Steam Guard")
        autoit.win_activate("Steam Guard")
        autoit.win_wait_active("Steam Guard")
        autoit.send(user.generate_auth_code())
        autoit.send('{ENTER}')


def use_last_used():
    if accounts.get_last_used() is not None:
        log_in(accounts.get_last_used())


def select_account():
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
                remove_account()
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
            elif accounts.get_users()[-1].set_shared_secret(shared_secret) is False:
                print('Invalid shared_secret')
            else:
                return

    accounts.add_user(User(
        not_none('username'),
        not_none('password'),
        None,
        False
    ))
    valid_shared_secret()
    write_json()


def remove_account():
    selection = int(input('Select an account to remove : '))
    accounts.delete_user(selection - 1)
    write_json()


def main():
    read_json()
    use_last_used()
    while True:
        select_account()


main()
