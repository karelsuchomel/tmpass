from datetime import datetime


# TODO, define for how long is password valid
def get_current_password():
    current_hour = int(datetime.now().strftime("%H"))
    return date_to_four_digits(current_hour)


# valid password in the next hour
def get_future_password():
    current_hour = int(datetime.now().strftime("%H"))
    return date_to_four_digits((current_hour + 1) % 24)


def date_to_four_digits(hour):
    today = datetime.now()
    date = today.strftime("%d%m%Y")

    # Linear Congruential Generator
    a = 1140671485
    c = 128201163
    m = 2 ** 24

    seed = int(str(hour) + date)
    rand = (a * seed + c) % m
    password = str(rand / m)

    return password[14:]


if __name__ == '__main__':
    print(get_current_password())
    print(get_future_password())
