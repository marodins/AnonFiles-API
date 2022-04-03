import random
from string import digits, ascii_letters
from hashlib import md5
from random import getrandbits


def generate_pass():
    return md5(str(getrandbits(10))).hexdigest()


def generate_name():
    return ''.join(random.choices(digits+ascii_letters, k=7))


def create_room(cache):
    room_pass = generate_pass()
    room_name = generate_name()

    while cache.get(room_name) is not None:
        room_name = generate_name()

    cache.set(room_name, room_pass)

    return room_name, room_pass

