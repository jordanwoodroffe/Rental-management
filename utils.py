"""
Houses utility methods used in MP application

used in date processing, password encryption, and file formatting
"""
import hashlib
import random
import string
from datetime import datetime

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def get_random_alphaNumeric_string(stringLength):
    """
    generates a random alphaNumeric string for salt value

    Args:
        stringLength: length of random string

    Returns:
        str: generated string of desired length
    """
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join((random.choice(lettersAndDigits) for i in range(stringLength)))


def hash_password(password, salt):
    """hashes a password for storing in database

    Args:
        password: plaintext password to hash
        salt: salt to hash with password

    Returns:
        hash & salt of input password
    """
    saltedpassword = password + salt
    password = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
    return password.hex()


def verify_password(stored_password, test_password, salt):
    """verifies that a password matches the encrypted password

    Args:
        stored_password: stored encrypted password
        test_password: password to test against
        salt: salt to encode with

    Returns:
        boolean: value indicating successful match
    """
    test_password = hashlib.pbkdf2_hmac('sha256', test_password.encode(), salt.encode(), 100000)
    if test_password.hex() == stored_password:
        return True
    return False


def compare_dates(d_start: datetime, d_end: datetime, b_start: datetime, b_end: datetime) -> bool:
    """Compares dates to see if there is an overlap. An overlaps occur if the proposed booking starts before/at the end
    of an  existing booking, or if the end of the proposed booking occurs after the start of an existing booking,
    or if both the proposed bookings start and end dates are respectively greater than or less than existing bookings

    Args:
        d_start: proposed booking start datetime
        d_end: proposed booking end datetime
        b_start: an existing bookings start
        b_end: an existing bookings end

    Returns:
        boolean: value indicating whether an overlap occurred: True if there was an overlap
    """
    if b_start <= d_end <= b_end:
        return True
    elif d_start <= b_end <= d_end:
        return True
    elif d_start <= b_start and d_end >= b_end:
        return True
    elif b_start <= d_start and b_end >= d_end:
        return True
    else:
        return False


def calc_hours(d1: datetime, d2: datetime) -> int:
    """
    Calculates the number of hours between two dates

    Args:
        d1: first date to compare
        d2: second date to compare

    Returns:
        int: abs value of hours between the two dates (an int)
    """
    diff = d1 - d2
    days, seconds = diff.days, diff.seconds
    hours = abs(days * 24 + seconds // 3600)
    return hours


def allowed_file(filename):
    """
    Checks if a filename matches any in an allowed extensions list

    Args:
        filename: filename to check

    Returns:
        boolean: value indicating if found in allowed extensions
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    start = datetime(2020, 11, 11, 10, 00, 00)
    end = datetime(2020, 12, 12, 13, 00, 00)
    print(calc_hours(start, end))
    b_start = datetime(2020, 11, 11, 11, 00, 00)
    b_end = datetime(2020, 11, 11, 11, 30, 00)
    print(start <= b_start and end >= b_end)
    d_start = datetime(2022, 5, 23, 20, 00, 00)
    d_end = datetime(2022, 5, 23, 20, 30, 00)
    b_start = datetime(2022, 5, 23, 20, 31, 00)
    b_end = datetime(2022, 5, 23, 20, 40, 00)
    print(compare_dates(d_start, d_end, b_start, b_end))
