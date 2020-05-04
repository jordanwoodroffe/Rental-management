import random, string, hashlib

def get_random_alphaNumeric_string(stringLength):
  lettersAndDigits = string.ascii_letters + string.digits
  return ''.join((random.choice(lettersAndDigits) for i in range(stringLength)))

def hash_password(password, salt):
  saltedpassword = password + salt
  password=hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
  return password.hex()

def verify_password(stored_password, test_password, salt):
  test_password = hashlib.pbkdf2_hmac('sha256', test_password.encode(), salt.encode(), 100000)
  if (test_password.hex() == stored_password):
    return True
  return False
