from hashlib import md5
from random import getrandbits


def generate_pass():
    return md5(str(getrandbits(10))).hexdigest()

