from Main import obtain_keys, read_data, select_account


def main(data):
    data = read_data(data[0], data[1])
    while True:
        select_account(data[0], data[1])


main(obtain_keys())