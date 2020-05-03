import random
import string

def get_random_alphaNumeric_string(stringLength):
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join((random.choice(lettersAndDigits) for i in range(stringLength)))
