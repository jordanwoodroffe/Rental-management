import random, string, hashlib
from datetime import datetime

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def get_random_alphaNumeric_string(stringLength):
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join((random.choice(lettersAndDigits) for i in range(stringLength)))


def hash_password(password, salt):
    saltedpassword = password + salt
    password = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
    return password.hex()


def verify_password(stored_password, test_password, salt):
    test_password = hashlib.pbkdf2_hmac('sha256', test_password.encode(), salt.encode(), 100000)
    if test_password.hex() == stored_password:
        return True
    return False


def compare_dates(start: datetime, end: datetime, b_start: datetime, b_end: datetime) -> bool:
    """
    Compares dates
    Args:
        start: proposed booking start datetime
        end: proposed booking end datetime
        b_start: an existing bookings start
        b_end: an existing bookings end

    Returns:
        a boolean value indicating whether an overlap occurred
    """
    return True if (start <= b_end) or (end >= b_start) or (start >= b_start and end <= b_end) else False


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    start = datetime(2020, 11, 11, 10, 00, 00)
    end = datetime(2020, 11, 11, 12, 00, 00)
    b_start = datetime(2020, 11, 11, 11, 00, 00)
    b_end = datetime(2020, 11, 11, 11, 30, 00)
    print(start <= b_start and end >= b_end)
