import random, string, hashlib
from datetime import datetime

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def get_random_alphaNumeric_string(stringLength):
    """

    Args:
        stringLength:

    Returns:

    """
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join((random.choice(lettersAndDigits) for i in range(stringLength)))


def hash_password(password, salt):
    """

    Args:
        password:
        salt:

    Returns:

    """
    saltedpassword = password + salt
    password = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
    return password.hex()


def verify_password(stored_password, test_password, salt):
    """

    Args:
        stored_password:
        test_password:
        salt:

    Returns:

    """
    test_password = hashlib.pbkdf2_hmac('sha256', test_password.encode(), salt.encode(), 100000)
    if test_password.hex() == stored_password:
        return True
    return False


def compare_dates(d1: datetime, d2: datetime, b_start: datetime, b_end: datetime) -> bool:
    """
    Compares dates
    Args:
        d1: proposed booking start datetime
        d2: proposed booking end datetime
        b_start: an existing bookings start
        b_end: an existing bookings end

    Returns:
        a boolean value indicating whether an overlap occurred
    """
    return True if (d1 <= b_end) or (d2 >= b_start) or (d1 >= b_start and d2 <= b_end) else False


def calc_hours(d1: datetime, d2: datetime) -> int:
    diff = d1 - d2
    days, seconds = diff.days, diff.seconds
    hours = abs(days * 24 + seconds // 3600)
    return hours


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    start = datetime(2020, 11, 11, 10, 00, 00)
    end = datetime(2020, 12, 12, 13, 00, 00)
    calc_hours(start, end)
    # b_start = datetime(2020, 11, 11, 11, 00, 00)
    # b_end = datetime(2020, 11, 11, 11, 30, 00)
    # print(start <= b_start and end >= b_end)
