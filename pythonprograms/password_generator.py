# Taken from: https://www.rosettacode.org/wiki/Password_generator#Python

import random
 
lowercase = 'abcdefghijklmnopqrstuvwxyz' # same as string.ascii_lowercase
uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' # same as string.ascii_uppercase
digits = '0123456789'                    # same as string.digits
punctuation = '!"#$%&\'()*+,-./:;<=>?@[]^_{|}~' # like string.punctuation but without backslash \ nor grave `
 
allowed = lowercase + uppercase + digits + punctuation
 
visually_similar = 'Il1O05S2Z'
 
 
def new_password(length:int, readable=True) -> str:
    if length < 4:
        print("password length={} is too short,".format(length),
            "minimum length=4")
        return ''
    choice = random.SystemRandom().choice
    while True:
        password_chars = [
            choice(lowercase),
            choice(uppercase),
            choice(digits),
            choice(punctuation)
            ] + random.sample(allowed, length-4)
        if (not readable or 
                all(c not in visually_similar for c in password_chars)):
            random.SystemRandom().shuffle(password_chars)
            return ''.join(password_chars)
 
 
def password_generator(length, qty=1, readable=True):
    for i in range(qty):
        print(new_password(length, readable))

def print(*args, **kwargs):
    pass

random.seed(893476598234587623485723487562)
n = 3000
password_generator(30, n)
password_generator(30, n, readable=False)

